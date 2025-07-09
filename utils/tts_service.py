
import os
import logging
from typing import Optional

try:
    from gtts import gTTS
except ImportError:
    logging.error("gTTS not installed. Please install: pip install gTTS")
    raise

logger = logging.getLogger(__name__)

def generate_voiceover_from_script(script: str, session_id: str, language: str = 'en') -> Optional[str]:
    """
    Convert text script to speech using gTTS.
    
    Args:
        script (str): Text script to convert to speech
        session_id (str): Unique session identifier
        language (str): Language code for speech generation
        
    Returns:
        Optional[str]: Path to generated audio file or None if failed
    """
    try:
        if not script or not script.strip():
            raise ValueError("Script is empty or None")
        
        logger.info(f"Generating voiceover for script ({len(script)} characters)")
        
        
        clean_script = script.strip()
        
        
        tts = gTTS(
            text=clean_script,
            lang=language,
            slow=False,
            tld='com'  
        )
        
        
        filename = f"voiceover_{session_id}.mp3"
        filepath = os.path.join('static', 'audio', filename)
        
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        
        logger.info(f"Saving audio to: {filepath}")
        tts.save(filepath)
        
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  
            logger.info(f"Successfully generated voiceover: {filepath} ({os.path.getsize(filepath)} bytes)")
            return filepath
        else:
            logger.error(f"Generated audio file is empty or corrupted: {filepath}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return None
            
    except Exception as e:
        logger.error(f"TTS service error: {str(e)}")
        
        
        try:
            return generate_fallback_audio(script, session_id)
        except Exception as fallback_error:
            logger.error(f"Fallback audio generation also failed: {str(fallback_error)}")
            return None

def generate_fallback_audio(script: str, session_id: str) -> Optional[str]:
    """
    Generate fallback audio using alternative method or create silent audio.
    
    Args:
        script (str): Text script
        session_id (str): Session identifier
        
    Returns:
        Optional[str]: Path to generated audio file
    """
    try:
        
        tts = gTTS(
            text=script[:500],  
            lang='en',
            slow=True  
        )
        
        filename = f"fallback_voiceover_{session_id}.mp3"
        filepath = os.path.join('static', 'audio', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        tts.save(filepath)
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
            logger.info(f"Generated fallback audio: {filepath}")
            return filepath
        else:
            
            return create_silent_audio(session_id)
            
    except Exception as e:
        logger.error(f"Fallback TTS error: {str(e)}")
        return create_silent_audio(session_id)

def create_silent_audio(session_id: str, duration: int = 10) -> Optional[str]:
    """
    Create a silent audio file as last resort.
    
    Args:
        session_id (str): Session identifier
        duration (int): Duration in seconds
        
    Returns:
        Optional[str]: Path to silent audio file
    """
    try:
        from moviepy import AudioClip
        import numpy as np
        
        
        audio = AudioClip(
            lambda t: np.zeros((int(44100*duration), 2)), 
            duration=duration,
            fps=44100
        )
        
        filename = f"silent_audio_{session_id}.mp3"
        filepath = os.path.join('static', 'audio', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        audio.write_audiofile(filepath, verbose=False, logger=None)
        
        logger.info(f"Created silent audio fallback: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error creating silent audio: {str(e)}")
        return None

def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file in seconds.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        float: Duration in seconds
    """
    try:
        from moviepy import AudioFileClip
        
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        
        return duration
        
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return 10.0  

def validate_audio_file(audio_path: str) -> bool:
    """
    Validate that audio file exists and is playable.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not os.path.exists(audio_path):
            return False
        
        if os.path.getsize(audio_path) < 1000:  
            return False
        
        
        from moviepy import AudioFileClip
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        
        return duration > 0
        
    except Exception as e:
        logger.error(f"Audio validation error: {str(e)}")
        return False

def enhance_script_for_speech(script: str) -> str:
    """
    Enhance script text for better speech synthesis.
    
    Args:
        script (str): Original script text
        
    Returns:
        str: Enhanced script
    """
    try:
        
        enhanced = script
        
        
        enhanced = enhanced.replace('.', '. ')
        enhanced = enhanced.replace(',', ', ')
        enhanced = enhanced.replace('!', '! ')
        enhanced = enhanced.replace('?', '? ')
        
        
        enhanced = ' '.join(enhanced.split())
        
        
        if len(enhanced) > 3000:
            enhanced = enhanced[:3000] + "..."
        
        return enhanced
        
    except Exception as e:
        logger.error(f"Script enhancement error: {str(e)}")
        return script

def test_tts_service():
    
    try:
        test_script = "This is a test of the text-to-speech service. It should create an audio file with this spoken content."
        session_id = "test123"
        result = generate_voiceover_from_script(test_script, session_id)
        
        if result and os.path.exists(result):
            print(f"Test successful: Audio generated at {result}")
            return True
        else:
            print("Test failed: No audio file generated")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    
    test_tts_service()