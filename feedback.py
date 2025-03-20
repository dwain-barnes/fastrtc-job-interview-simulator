"""
Feedback system for job interview training application.
This module provides detailed, actionable feedback on interview performance.
"""

import json
from openai import AsyncOpenAI
from settings import get_settings

settings = get_settings()
llm_client = AsyncOpenAI(api_key=settings.LLM_API_KEY.get_secret_value(), base_url=settings.LLM_BASE_URL)

FEEDBACK_PROMPT = """
Analyze the following job interview transcript and provide detailed professional feedback as an expert in interview coaching and career development.

The feedback should include:

1. A numerical score from 1 to 10
2. A concise summary of the overall performance (2-3 sentences)
3. A list of 2-4 strengths demonstrated in the interview
4. Detailed analysis of areas for improvement in the following categories:
   a. Introduction and first impression
   b. Response quality and structure
   c. Technical knowledge demonstration
   d. Soft skills and communication
   e. Questions asked to the interviewer
5. 3-5 specific, actionable recommendations for improvement

Format the response as a structured JSON with the following fields:
{
  "score": number,
  "summary": string,
  "strengths": [list of strings],
  "areas_for_improvement": {
    "introduction": [list of strings],
    "response_quality": [list of strings],
    "technical_knowledge": [list of strings],
    "communication": [list of strings],
    "questions_to_interviewer": [list of strings]
  },
  "recommendations": [list of strings]
}

Be specific, objective, and educational in your feedback. Focus on providing actionable guidance that helps the candidate improve their interview skills.

Transcript:
"""

async def generate_detailed_feedback(transcript: str) -> dict:
    """
    Generate detailed feedback for a job interview transcript using AI.
    Returns a structured feedback object with score and analysis.
    """
    prompt = FEEDBACK_PROMPT + transcript
    
    try:
        # Use AsyncOpenAI client for detailed feedback
        completion = await llm_client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        feedback_text = completion.choices[0].message.content
        feedback_data = json.loads(feedback_text)
        
        # Ensure all expected fields are present
        feedback_data.setdefault("score", 5)
        feedback_data.setdefault("summary", "No summary provided.")
        feedback_data.setdefault("strengths", [])
        
        if "areas_for_improvement" not in feedback_data:
            feedback_data["areas_for_improvement"] = {}
        
        areas = feedback_data["areas_for_improvement"]
        areas.setdefault("introduction", [])
        areas.setdefault("response_quality", [])
        areas.setdefault("technical_knowledge", [])
        areas.setdefault("communication", [])
        areas.setdefault("questions_to_interviewer", [])
        
        feedback_data.setdefault("recommendations", [])
        
        return feedback_data
        
    except Exception as e:
        print(f"Error generating detailed feedback: {str(e)}")
        # Return a basic feedback structure if the API call fails
        return {
            "score": 5,
            "summary": "Unable to generate detailed feedback due to a technical error.",
            "strengths": ["Participated in the interview"],
            "areas_for_improvement": {
                "introduction": ["No assessment available"],
                "response_quality": ["No assessment available"],
                "technical_knowledge": ["No assessment available"],
                "communication": ["No assessment available"],
                "questions_to_interviewer": ["No assessment available"]
            },
            "recommendations": ["Try again when the system is functioning properly."]
        }