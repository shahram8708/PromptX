# PromptX

PromptX is a Flask-based web application that automatically generates short videos from a text prompt. It uses AI to create a narrative script, converts the script to voice-over audio, fetches relevant stock footage, synchronizes everything together, and produces a final merged video ready to download.

The system combines AI content generation, text-to-speech, stock video retrieval, and video editing automation with logging, status tracking, and a clean web interface.

---

## Features

* Generate video scripts using Google Gemini AI
* Extract relevant keywords automatically
* Fetch stock videos based on AI-generated keywords
* Convert generated script to voice-over using gTTS
* Merge multiple clips, audio, and subtitles into a single video using MoviePy
* Download final rendered video
* Session-based processing with unique identifiers
* Progress logging
* Error handling and fallback behavior
* Web interface built with Flask and Jinja templates

---

## Tech Stack

**Backend**

* Flask
* Python 3
* google-genai
* gTTS
* Requests
* MoviePy
* NumPy
* python-dotenv

**Frontend**

* HTML / Jinja Templates
* CSS
* JavaScript

**Other**

* Logging system
* File storage for generated media

All dependencies are listed in `requirements.txt`.

---

## Project Structure

```
PromptX/
│
├── app.py                   # Main Flask application
├── requirements.txt         # Project dependencies
├── logs/
│   └── app.log              # Application logs
├── static/
│   ├── audio/               # Generated audio
│   ├── css/
│   ├── images/
│   ├── js/
│   └── final/               # Final rendered videos
├── templates/               # Jinja HTML templates
└── utils/
    ├── ai_service.py        # AI video script + keyword generation
    ├── tts_service.py       # Text-to-speech processing
    ├── video_service.py     # Stock video fetching
    └── video_processor.py   # Video merging and processing
```

---

## Installation

1. Clone or extract the project.
2. Create a Python virtual environment (recommended).
3. Install dependencies:

```
pip install -r requirements.txt
```

---

## Configuration

PromptX expects valid API credentials to function correctly.

Environment variables are loaded using `python-dotenv`. Create a `.env` file in the project root and configure the following (based on code expectations):

```
GEMINI_API_KEY=your_google_gemini_key
GOOGLE_API_KEY=your_google_gemini_key
```

The application currently integrates with:

* Google Gemini API (for AI script + keywords)
* gTTS for speech generation
* Pexels API usage is implemented in `video_service.py` logic

Ensure your credentials are correct for generation to succeed.

Logging output is stored in:

```
logs/app.log
```

---

## Running the Application

Start the Flask app:

```
python app.py
```

By default the server runs on port 5000.

Open the application in a browser:

```
http://localhost:5000
```

---

## Usage

1. Open the homepage.
2. Enter a topic or prompt.
3. Submit the form.
4. The app performs:

   * AI script generation
   * Keyword extraction
   * Stock video fetching
   * Voice-over generation
   * Video merging
5. Once completed, a results page provides a download link for the final video.

A session ID is created for each generation process.

Progress and operational flow are logged for debugging.

---

## API / Routes

| Route                  | Method | Description            |
| ---------------------- | ------ | ---------------------- |
| `/`                    | GET    | Home page              |
| `/generate`            | POST   | Generate video process |
| `/download/<filename>` | GET    | Download final video   |
| `/status/<session_id>` | GET    | Session status         |

---

## Troubleshooting

* Ensure API keys are valid.
* Confirm dependencies are installed.
* Check `logs/app.log` for detailed error info.
* Ensure internet connectivity for AI, TTS, and video fetching.
* Some failures may occur if no suitable stock videos are found.
* Large or empty prompts may affect AI output quality.

---

## Notes

* Uses session-based storage under `static/audio` and `static/final`.
* Error pages and fallback handling are included.
* The system is designed for experimentation and prototyping workflows.

---

## License

This project does not include a license file in the repository.
