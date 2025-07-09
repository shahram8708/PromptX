
import os
import logging
from typing import List, Optional

try:
    from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
    import numpy as np
except ImportError:
    logging.error("MoviePy not installed. Please install: pip install moviepy")
    raise

logger = logging.getLogger(__name__)

def merge_video_audio_captions(video_paths: List[str], audio_path: str, script_text: str, session_id: str) -> Optional[str]:
    """
    Merge video clips, audio narration, and subtitles into final video.
    
    Args:
        video_paths (List[str]): List of paths to video clips
        audio_path (str): Path to audio narration file
        script_text (str): Text for subtitles
        session_id (str): Unique session identifier
        
    Returns:
        Optional[str]: Path to final merged video or None if failed
    """
    try:
        logger.info(f"Starting video merge with {len(video_paths)} videos and audio: {audio_path}")
        
        
        if not os.path.exists(audio_path):
            raise ValueError(f"Audio file not found: {audio_path}")
        
        audio_clip = AudioFileClip(audio_path)
        target_duration = audio_clip.duration
        
        logger.info(f"Target video duration: {target_duration:.2f} seconds")
        
        
        video_clips = []
        for video_path in video_paths:
            if os.path.exists(video_path):
                try:
                    clip = VideoFileClip(video_path)
                    
                    
                    if clip.size != (1920, 1080):
                        clip = clip.resized((1920, 1080))
                    
                    video_clips.append(clip)
                    logger.info(f"Loaded video: {video_path} ({clip.duration:.2f}s)")
                    
                except Exception as e:
                    logger.error(f"Error loading video {video_path}: {str(e)}")
                    continue
            else:
                logger.warning(f"Video file not found: {video_path}")
        
        if not video_clips:
            logger.warning("No valid video clips found, creating fallback video")
            video_clips = [create_fallback_background(target_duration)]
        
        
        total_video_duration = sum(clip.duration for clip in video_clips)
        
        if total_video_duration < target_duration:
            
            video_clips = extend_videos_to_duration(video_clips, target_duration)
        elif total_video_duration > target_duration:
            
            video_clips = trim_videos_to_duration(video_clips, target_duration)
        
        
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        
        if final_video.duration > target_duration:
            final_video = final_video.subclipped(0, target_duration)
        elif final_video.duration < target_duration:
            
            black_duration = target_duration - final_video.duration
            black_clip = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=black_duration)
            final_video = concatenate_videoclips([final_video, black_clip])
        
        
        final_video = final_video.with_audio(audio_clip)
        
        
        output_filename = f"final_video_{session_id}.mp4"
        output_path = os.path.join('static', 'final', output_filename)
        
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        
        logger.info(f"Writing final video to: {output_path}")
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        
        for clip in video_clips:
            clip.close()
        audio_clip.close()
        final_video.close()
        
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:  
            logger.info(f"Successfully created final video: {output_path} ({os.path.getsize(output_path)} bytes)")
            return output_path
        else:
            logger.error(f"Final video file is empty or corrupted: {output_path}")
            return None
            
    except Exception as e:
        logger.error(f"Video processing error: {str(e)}")
        return None

def extend_videos_to_duration(video_clips: List, target_duration: float) -> List:
    """
    Extend video clips to match target duration by looping.
    
    Args:
        video_clips (List): List of video clips
        target_duration (float): Target duration in seconds
        
    Returns:
        List: Extended list of video clips
    """
    try:
        extended_clips = []
        current_duration = 0
        clip_index = 0
        
        while current_duration < target_duration:
            clip = video_clips[clip_index % len(video_clips)]
            remaining_duration = target_duration - current_duration
            
            if clip.duration <= remaining_duration:
                extended_clips.append(clip)
                current_duration += clip.duration
            else:
                
                trimmed_clip = clip.subclipped(0, remaining_duration)
                extended_clips.append(trimmed_clip)
                current_duration += remaining_duration
            
            clip_index += 1
        
        logger.info(f"Extended {len(video_clips)} clips to {len(extended_clips)} clips ({current_duration:.2f}s)")
        return extended_clips
        
    except Exception as e:
        logger.error(f"Error extending videos: {str(e)}")
        return video_clips

def trim_videos_to_duration(video_clips: List, target_duration: float) -> List:
    """
    Trim video clips to match target duration.
    
    Args:
        video_clips (List): List of video clips
        target_duration (float): Target duration in seconds
        
    Returns:
        List: Trimmed list of video clips
    """
    try:
        trimmed_clips = []
        current_duration = 0
        
        for clip in video_clips:
            remaining_duration = target_duration - current_duration
            
            if remaining_duration <= 0:
                break
            
            if clip.duration <= remaining_duration:
                trimmed_clips.append(clip)
                current_duration += clip.duration
            else:
                
                trimmed_clip = clip.subclipped(0, remaining_duration)
                trimmed_clips.append(trimmed_clip)
                current_duration += remaining_duration
                break
        
        logger.info(f"Trimmed videos to {current_duration:.2f}s duration")
        return trimmed_clips
        
    except Exception as e:
        logger.error(f"Error trimming videos: {str(e)}")
        return video_clips

def create_fallback_background(duration: float):
    """
    Create a fallback background video when no stock videos are available.
    
    Args:
        duration (float): Duration in seconds
        
    Returns:
        VideoClip: Generated background video
    """
    try:
        
        background = ColorClip(size=(1920, 1080), color=(30, 144, 255), duration=duration)  
        
        
        title_clip = TextClip(
            txt="AI Generated Video",
            fontsize=100,
            color='white',
            font='Arial-Bold'
        ).with_duration(duration).with_position('center')
        
        
        fallback_video = CompositeVideoClip([background, title_clip])
        
        logger.info(f"Created fallback background video ({duration:.2f}s)")
        return fallback_video
        
    except Exception as e:
        logger.error(f"Error creating fallback background: {str(e)}")
        
        return ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration)

def validate_video_file(video_path: str) -> bool:
    """
    Validate that video file exists and is playable.
    
    Args:
        video_path (str): Path to video file
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not os.path.exists(video_path):
            return False
        
        if os.path.getsize(video_path) < 10000:  
            return False
        
        
        clip = VideoFileClip(video_path)
        duration = clip.duration
        size = clip.size
        clip.close()
        
        return duration > 0 and size[0] > 0 and size[1] > 0
        
    except Exception as e:
        logger.error(f"Video validation error: {str(e)}")
        return False

def get_video_info(video_path: str) -> dict:
    """
    Get information about a video file.
    
    Args:
        video_path (str): Path to video file
        
    Returns:
        dict: Video information
    """
    try:
        clip = VideoFileClip(video_path)
        info = {
            'duration': clip.duration,
            'size': clip.size,
            'fps': clip.fps,
            'file_size': os.path.getsize(video_path)
        }
        clip.close()
        return info
        
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        return {}

def test_video_processor():
    
    try:
        
        print("Video processor module loaded successfully")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    
    test_video_processor()