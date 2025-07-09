
"""
Utility modules for the AI Video Generator application.

This package contains:
- ai_service: Google Gemini Flash API integration
- video_service: Pexels/Pixabay video fetching
- tts_service: Google Text-to-Speech integration  
- video_processor: MoviePy video processing and merging
"""

__version__ = "1.0.0"


from .ai_service import generate_script_from_prompt
from .video_service import fetch_videos_from_keywords
from .tts_service import generate_voiceover_from_script
from .video_processor import merge_video_audio_captions

__all__ = [
    'generate_script_from_prompt',
    'fetch_videos_from_keywords', 
    'generate_voiceover_from_script',
    'merge_video_audio_captions'
]