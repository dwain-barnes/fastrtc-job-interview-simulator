import json
import os
import time
from pathlib import Path
import asyncio

import gradio as gr
import numpy as np
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastrtc import (
    AdditionalOutputs,
    ReplyOnPause,
    Stream,
    get_twilio_turn_credentials,
    AlgoOptions,
    SileroVadOptions
)
from fastrtc.utils import audio_to_bytes
from gradio.utils import get_space
from pydantic import BaseModel
from speech import SpeechClient
from settings import get_settings
from openai import AsyncOpenAI
from feedback import generate_detailed_feedback

# Import scenario prompting helpers
from scenario_prompting import get_base_scenario_prompt, get_interviewer_system_prompt, save_dynamic_prompt

settings = get_settings()
speech_client = SpeechClient(
    stt_base_url=settings.STT_BASE_URL,
    stt_model=settings.STT_MODEL,
    stt_api_key=settings.STT_API_KEY,
    stt_response_format=settings.STT_RESPONSE_FORMAT,
    tts_base_url=settings.TTS_BASE_URL,
    tts_api_key=settings.TTS_API_KEY,
    tts_model=settings.TTS_MODEL,
    tts_voice=settings.TTS_VOICE,
    tts_backend=settings.TTS_BACKEND,
    tts_audio_format=settings.TTS_AUDIO_FORMAT,
    language=settings.LANGUAGE,
)
llm_client = AsyncOpenAI(api_key=settings.LLM_API_KEY.get_secret_value(), base_url=settings.LLM_BASE_URL)
curr_dir = Path(__file__).parent
templates = Jinja2Templates(directory="templates")

# Global dictionary to store conversation logs by webrtc_id
conversation_logs = {}

def load_dynamic_prompt():
    """
    Load the dynamic system prompt generated for the interviewer.
    """
    prompt = os.environ.get("DYNAMIC_SYSTEM_PROMPT")
    if prompt:
        return prompt
    try:
        with open("dynamic_prompt.txt", "r") as f:
            prompt_data = json.loads(f.read())
            return prompt_data.get("prompt", "You are conducting a job interview. Ask professional questions and provide insightful feedback.")
    except Exception as e:
        print("Failed to load dynamic prompt:", e)
        return ("You are a hiring manager conducting a job interview. "
                "Ask relevant questions about the candidate's experience and skills. "
                "Be professional and thorough in your assessment.")

async def async_response(audio, chatbot=None, webrtc_id=None):
    """Asynchronous response function customized for job interviews."""
    chatbot = chatbot or []
    
    # Add system prompt if this is the first interaction
    if not chatbot or all(msg.get("role") != "system" for msg in chatbot):
        system_prompt = load_dynamic_prompt()
        chatbot.insert(0, {"role": "system", "content": system_prompt})
        
    messages = [{"role": d["role"], "content": d["content"]} for d in chatbot]
    
    # Process STT
    prompt = await speech_client.speech_to_text(("audio-file.mp3", audio_to_bytes(audio)))
    chatbot.append({"role": "user", "content": prompt})
    yield AdditionalOutputs(chatbot)
    
    # Store conversation in logs for scoring later if webrtc_id is provided
    if webrtc_id:
        conversation_logs[webrtc_id] = chatbot
    
    # Add the user's transcription to messages
    messages.append({"role": "user", "content": prompt})
    
    start = time.time()
    print("starting response pipeline", start)
    
    complete_response = ""
    sentence_buffer = ""
    
    stream_llm = await llm_client.chat.completions.create(
        model=settings.LLM_MODEL,
        max_tokens=512,
        messages=messages,
        temperature=0.7,  # Slightly higher temperature for more natural interviewer variation
        stream=True,
    )
    
    async for chunk in stream_llm:
        content = chunk.choices[0].delta.content
        if content is None:
            continue
            
        complete_response += content
        sentence_buffer += content
        
        if any(char in content for char in ['.', '!', '?', '\n']) and len(sentence_buffer) > 15:
            async for audio_data in speech_client.text_to_speech_stream(sentence_buffer):
                yield audio_data
            sentence_buffer = ""
    
    if sentence_buffer:
        async for audio_data in speech_client.text_to_speech_stream(sentence_buffer):
            yield audio_data
    
    chatbot.append({"role": "assistant", "content": complete_response})
    yield AdditionalOutputs(chatbot)
    
    if webrtc_id:
        conversation_logs[webrtc_id] = chatbot
        
    print("finished response pipeline", time.time() - start)


def response(audio: tuple[int, np.ndarray], chatbot: list[dict] | None = None):
    """Synchronous wrapper for the asynchronous response generator."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Get the webrtc_id from the response function attribute (set in /input_hook)
    webrtc_id = getattr(response, 'webrtc_id', None)
    
    try:
        # Pass webrtc_id explicitly to async_response
        agen = async_response(audio, chatbot, webrtc_id=webrtc_id)
        
        while True:
            try:
                item = loop.run_until_complete(agen.__anext__())
                yield item
            except StopAsyncIteration:
                break
            except Exception as e:
                print(f"Error in response generator: {e}")
                continue
    finally:
        loop.close()

chatbot_component = gr.Chatbot(type="messages")
stream = Stream(
    handler=ReplyOnPause(
        response,
        algo_options=AlgoOptions(
            audio_chunk_duration=1.2,
            started_talking_threshold=0.2,  # Increase threshold so detection starts only when you're clearly speaking
            speech_threshold=0.4          # Raise threshold to avoid triggering on brief pauses
        ),
        model_options=SileroVadOptions(
            threshold=0.5,
            min_speech_duration_ms=250,
            min_silence_duration_ms=2000  # Require 2 seconds of silence before replying
        ),
        can_interrupt=False  # Disable interruption so that the AI won't cut you off
    ),
    modality="audio",
    mode="send-receive",
    additional_outputs_handler=lambda a, b: b,
    additional_inputs=[chatbot_component],
    additional_outputs=[chatbot_component],
    rtc_configuration=get_twilio_turn_credentials() if get_space() else None,
    concurrency_limit=5 if get_space() else None,
    time_limit=90 if get_space() else None,
)


class Message(BaseModel):
    role: str
    content: str


class InputData(BaseModel):
    webrtc_id: str
    chatbot: list[Message]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
stream.mount(app)

# Main routes for job interview system
@app.get("/")
async def index(request: Request):
    """Serve the job setup page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request, 
    job_description: str = Form(...),
    position_title: str = Form(...),
    industry: str = Form(...),
    difficulty: str = Form("medium"),
    technical: bool = Form(False),
    behavioral: bool = Form(True)
):
    """Generate job interview scenario using the AsyncOpenAI client"""
    # Create an optimized prompt with examples for the job interview scenario
    prompt = get_base_scenario_prompt(
        job_description, 
        position_title, 
        industry, 
        difficulty, 
        technical, 
        behavioral
    )

    try:
        # Use AsyncOpenAI client to generate the briefing
        completion = await llm_client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        briefing_html = completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating briefing: {str(e)}")
        briefing_html = "<p>Error connecting to the language model. Please try again.</p>"
    
    # Create the dynamic system prompt for the interview
    system_prompt = get_interviewer_system_prompt(
        job_description, 
        position_title, 
        industry, 
        difficulty, 
        technical, 
        behavioral
    )
    
    # Save the dynamic system prompt
    scenario_data = {
        "difficulty": difficulty,
        "position_title": position_title,
        "industry": industry,
        "technical": technical,
        "behavioral": behavioral
    }
    save_dynamic_prompt(scenario_data, system_prompt)
    
    # Generate a unique webrtc_id for this interview session
    webrtc_id = f"interview_{int(time.time())}"
    
    # Render the briefing page
    return templates.TemplateResponse(
        "briefing.html", 
        {
            "request": request, 
            "briefing": briefing_html,
            "difficulty": difficulty,
            "position": position_title,
            "webrtc_id": webrtc_id
        }
    )

@app.get("/interview")
async def interview_page(request: Request, webrtc_id: str):
    """Render the interview interface with the correct WebRTC ID"""
    rtc_config = get_twilio_turn_credentials() if get_space() else None
    
    return templates.TemplateResponse(
        "interview.html", 
        {
            "request": request,
            "webrtc_id": webrtc_id,
            "rtc_config": json.dumps(rtc_config)
        }
    )

@app.post("/input_hook")
async def input_hook(body: InputData):
    """Process input from frontend and set it for the RTC stream"""
    webrtc_id = body.webrtc_id
    conv = body.model_dump()["chatbot"]
    conversation_logs[webrtc_id] = conv
    stream.set_input(webrtc_id, conv)
    
    # Store webrtc_id on the response function
    setattr(response, 'webrtc_id', webrtc_id)
    
    return {"status": "ok"}


@app.get("/outputs")
def outputs(webrtc_id: str):
    """Stream outputs from the RTC session to the frontend"""
    async def output_stream():
        async for output in stream.output_stream(webrtc_id):
            chatbot = output.args[0]
            conversation_logs[webrtc_id] = chatbot
            yield f"event: output\ndata: {json.dumps(chatbot[-1])}\n\n"
    return StreamingResponse(output_stream(), media_type="text/event-stream")

@app.get("/score")
async def score(webrtc_id: str):
    """Retrieve, score, and provide detailed feedback for the interview transcript"""
    conv = conversation_logs.get(webrtc_id, [])
    transcript_lines = []
    for msg in conv:
        if msg['role'] != 'system':
            transcript_lines.append(f"{msg['role'].capitalize()}: {msg['content']}")
    
    transcript = "\n".join(transcript_lines)
    
    feedback = await generate_detailed_feedback(transcript)
    
    result = {
        "transcript": transcript, 
        "score": feedback["score"],
        "feedback": feedback
    }
    
    return result

@app.get("/voice")
async def voice_chat():
    """Legacy entry point for just the voice chat functionality"""
    rtc_config = get_twilio_turn_credentials() if get_space() else None
    html_content = (curr_dir / "index_voice.html").read_text()
    html_content = html_content.replace("__RTC_CONFIGURATION__", json.dumps(rtc_config))
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    if (mode := settings.MODE) == "UI":
        stream.ui.launch(server_port=7860, server_name="0.0.0.0")
    elif mode == "PHONE":
        stream.fastphone(host="0.0.0.0", port=7860)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=7860)