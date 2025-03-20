# Job Interview Simulator

<p align="center">
  <img src="https://placeholder-for-logo.com/job-interview-simulator-logo.png" alt="Job Interview Simulator Logo" width="200"/>
</p>

<p align="center">
  A FastRTC-powered job interview simulator with real-time voice interaction that helps job seekers practice and improve their interview skills. The application uses AI to create realistic interview scenarios based on specific job descriptions, with the AI playing the role of the interviewer. Users engage in natural voice conversations, receive immediate responses, and get detailed performance feedback after each session. With customisable difficulty levels and industry-specific questions, this tool provides a risk-free environment to build confidence and refine responses before real interviews.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

## Features

- 🎙️ **Real-time voice interaction** - Have natural conversations with an AI interviewer
- 💼 **Customizable job scenarios** - Practice for positions in various industries
- 🔄 **Multiple difficulty levels** - From beginner-friendly to stress interviews
- 💡 **Comprehensive feedback** - Get scored on your performance with actionable insights
- 📊 **Performance analytics** - Track your improvement over time
- 🧠 **Adaptive questioning** - Interviewer responds based on your answers
- 📝 **Interview transcripts** - Review the full conversation afterward

## Demo

![Demo GIF](https://placeholder-for-demo.com/job-interview-simulator-demo.gif)

👉 [Try the live demo](https://your-demo-url.com) (if available)

## How It Works

Job Interview Simulator uses WebRTC for real-time voice communication and AI language models to create realistic interview experiences:

1. **Setup** - Enter job description, position details, and select interview difficulty
2. **Briefing** - Review the generated job scenario and interview context
3. **Interview** - Engage in a voice conversation with the AI interviewer
4. **Feedback** - Receive detailed assessment and actionable improvement recommendations

<p align="center">
  <img src="https://placeholder-for-workflow.com/workflow-diagram.png" alt="Workflow Diagram" width="600"/>
</p>

## Installation

### Prerequisites

- Python 3.9+
- Node.js 14+ (for frontend development)
- FFmpeg (for audio processing)

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/username/job-interview-simulator.git
cd job-interview-simulator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```
# LLM configuration
LLM_BASE_URL=https://your-llm-api-url.com
LLM_MODEL=your-model-name
LLM_API_KEY=your-api-key

# STT configuration
STT_BASE_URL=https://your-stt-api-url.com
STT_MODEL=your-stt-model
STT_API_KEY=your-stt-api-key
STT_RESPONSE_FORMAT=json
LANGUAGE=en

# TTS configuration
TTS_BASE_URL=https://your-tts-api-url.com
TTS_API_KEY=your-tts-api-key
TTS_MODEL=your-tts-model
TTS_VOICE=en-US-neural2-J
TTS_BACKEND=standard
TTS_AUDIO_FORMAT=mp3

# Application mode (UI, API, or PHONE)
MODE=UI
```

## Usage

### Starting the Server

```bash
python app.py
```

The application will be available at `http://localhost:7860`

### Creating an Interview

1. **Enter job details**: 
   - Paste the job description
   - Specify the position title
   - Select the industry
   - Choose difficulty level

2. **Start the interview**:
   - Review the briefing information
   - Click "Start Interview" when ready
   - Allow microphone access when prompted

3. **During the interview**:
   - Speak naturally into your microphone
   - Listen to the interviewer's questions
   - End the interview when finished

4. **Review feedback**:
   - See your overall score
   - Review strengths and areas for improvement
   - Get specific recommendations for future interviews

## Configuration

### Difficulty Levels

- **Easy**: Beginner-friendly questions with a supportive interviewer
- **Medium**: Standard professional interview with balanced questions
- **Hard**: Challenging questions requiring detailed answers
- **Expert**: Stress interview with rapid-fire questions and interruptions

### Question Types

- **Technical Questions**: Toggle on/off for role-specific technical assessment
- **Behavioral Questions**: Toggle on/off for soft skills and experience evaluation

## Tech Stack

- **Backend**: FastAPI, Python
- **Voice Processing**: WebRTC, SileroVAD
- **AI/ML**: OpenAI, Custom prompt engineering
- **Frontend**: HTML/CSS/JavaScript
- **Audio**: Speech-to-Text and Text-to-Speech APIs

## Project Structure

```
job-interview-simulator/
├── app.py                # Main application file
├── feedback.py           # Interview assessment logic
├── scenario_prompting.py # Interview scenario generation
├── settings.py           # Application settings
├── speech.py             # Speech processing
├── static/               # CSS, JavaScript, etc.
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── briefing.html     # Interview briefing page
│   └── interview.html    # Interview interface
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [OpenAI](https://openai.com/) for the language model capabilities
- [WebRTC](https://webrtc.org/) for real-time communication

---

<p align="center">
  Made with ❤️ for job seekers everywhere
</p>
