# AI Video Generator

A complete, production-ready web application that transforms text prompts into professional videos using AI. Built with Flask, Bootstrap 5, Google Gemini AI, and MoviePy.

## 🎬 Features

- **AI Script Generation**: Uses Google Gemini Flash API to create engaging video scripts
- **Stock Video Integration**: Automatically fetches relevant videos from Pexels API
- **AI Voice Narration**: Converts scripts to natural speech using Google Text-to-Speech
- **Automatic Video Assembly**: Merges videos, audio, and subtitles using MoviePy
- **Professional UI**: Modern, responsive interface built with Bootstrap 5
- **Real-time Progress**: Live status updates during video generation
- **Download & Share**: Easy video download and sharing capabilities

## 🚀 Live Demo

The application frontend is deployed and accessible at: 
https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/5c274288b713634fca8cc2757f422a48/ca83789e-a8ed-4165-bbf8-3c2bee89cb33/index.html

## 📁 Project Structure

```
ai-video-generator/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with Bootstrap 5
│   ├── index.html            # Landing page
│   ├── result.html           # Video results page
│   └── error.html            # Error handling page
├── static/                    # Static assets
│   ├── css/
│   │   └── custom.css        # Custom styling
│   ├── js/
│   │   └── script.js         # Client-side JavaScript
│   ├── videos/               # Temporary video storage
│   ├── audio/                # Temporary audio storage
│   └── final/                # Final video output
├── utils/                     # Backend utilities
│   ├── __init__.py
│   ├── ai_service.py         # Google Gemini API integration
│   ├── video_service.py      # Pexels/Pixabay video fetching
│   ├── tts_service.py        # gTTS text-to-speech
│   └── video_processor.py    # MoviePy video processing
└── logs/                      # Application logs
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- FFmpeg (for video processing)

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-video-generator.git
cd ai-video-generator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**Windows:**
- Download from https://ffmpeg.org/download.html
- Extract and add to PATH

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 5. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- **GEMINI_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **PEXELS_API_KEY**: Get from [Pexels API](https://www.pexels.com/api/)

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔑 API Keys Setup

### Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key to your `.env` file

### Pexels API Key

1. Visit [Pexels API](https://www.pexels.com/api/)
2. Sign up for a free account
3. Go to your account dashboard
4. Copy the API key to your `.env` file

## 📊 How It Works

### 1. User Input
User provides a detailed description of the video they want to create.

### 2. AI Script Generation
- Google Gemini Flash API processes the prompt
- Generates a professional script (150-300 words)
- Extracts 3-5 relevant keywords for video search

### 3. Video Asset Collection
- Searches Pexels API for stock videos using keywords
- Downloads relevant HD video clips
- Creates fallback videos if API fails

### 4. Audio Generation
- Converts script to natural speech using gTTS
- Optimizes audio for video synchronization
- Handles multiple languages and accents

### 5. Video Assembly
- Uses MoviePy to merge video clips
- Synchronizes audio with video duration
- Adds embedded subtitles
- Exports high-quality MP4 file

## 🎨 Customization

### Styling
- Edit `static/css/custom.css` for visual customization
- Modify Bootstrap variables for theme changes
- Update templates in `templates/` directory

### AI Behavior
- Adjust prompts in `utils/ai_service.py`
- Modify keyword extraction logic
- Change video search parameters

### Video Processing
- Configure video resolution and quality in `utils/video_processor.py`
- Adjust subtitle styling and positioning
- Modify audio processing settings

## 🚢 Deployment

### Production Server

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables for Production

```bash
# Required for production
SECRET_KEY=your-strong-secret-key
FLASK_ENV=production
FLASK_DEBUG=False

# API Keys
GEMINI_API_KEY=your-production-gemini-key
PEXELS_API_KEY=your-production-pexels-key

# Optional production settings
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
```

## 🔧 Troubleshooting

### Common Issues

**FFmpeg not found:**
- Ensure FFmpeg is installed and in PATH
- Restart terminal after installation

**API Rate Limits:**
- Pexels: 200 requests/hour (free tier)
- Gemini: Check your quota at Google AI Studio

**Large Video Files:**
- Adjust `MAX_CONTENT_LENGTH` in app.py
- Monitor disk space in `/static` directories

**Memory Issues:**
- Reduce video resolution in processor
- Implement file cleanup more aggressively

### Debug Mode

```bash
# Enable detailed logging
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG

python app.py
```

## 📈 Performance Optimization

### Video Processing
- Use lower resolution for faster processing
- Implement background task queues (Celery)
- Add video caching mechanisms

### API Optimization
- Implement request caching
- Add retry mechanisms with exponential backoff
- Use connection pooling for HTTP requests

### Storage
- Implement automatic file cleanup
- Use cloud storage (AWS S3) for large files
- Add compression for archived videos

## 🔒 Security Considerations

### API Keys
- Never commit API keys to version control
- Use environment variables for all secrets
- Rotate keys regularly

### File Uploads
- Validate file types and sizes
- Implement virus scanning for uploads
- Use secure file storage practices

### Rate Limiting
- Implement per-user rate limiting
- Add CAPTCHA for abuse prevention
- Monitor API usage patterns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/ai-video-generator/issues)
- **Documentation**: [Wiki](https://github.com/your-username/ai-video-generator/wiki)
- **Email**: support@aivideogenerator.com

## 🙏 Acknowledgments

- **Google Gemini AI** for script generation
- **Pexels** for free stock video content
- **MoviePy** for video processing capabilities
- **Bootstrap** for responsive UI components
- **Flask** for the web framework foundation

## 📊 Technology Stack

- **Backend**: Python, Flask, MoviePy, gTTS
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: Google Gemini Flash API
- **APIs**: Pexels Video API, Google Text-to-Speech
- **Video Processing**: FFmpeg, MoviePy
- **Deployment**: Gunicorn, Docker, Nginx

---

**Made with ❤️ for the AI community**