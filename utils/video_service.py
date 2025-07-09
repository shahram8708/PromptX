
import os
import requests
import logging
from typing import List
from pathlib import Path
import time

logger = logging.getLogger(__name__)

def fetch_videos_from_keywords(keywords: List[str], session_id: str) -> List[str]:
    """
    Fetch stock videos from Pexels API based on keywords.
    
    Args:
        keywords (List[str]): List of keywords to search for
        session_id (str): Unique session identifier
        
    Returns:
        List[str]: List of local video file paths
    """
    video_paths = []
    
    try:
        
        pexels_api_key = "BgCFqepDpjSeAqmFKaJg7IrEHgjcQSjGmBAXDhfVhPE4OnN8VmTykD9n"
        if not pexels_api_key:
            logger.warning("PEXELS_API_KEY not found, using fallback video fetching")
            return get_fallback_videos(keywords, session_id)
        
        headers = {
            'Authorization': pexels_api_key
        }
        
        
        for i, keyword in enumerate(keywords[:3]):  
            try:
                logger.info(f"Searching videos for keyword: {keyword}")
                
                
                search_url = f"https://api.pexels.com/videos/search"
                params = {
                    'query': keyword,
                    'per_page': 5,
                    'orientation': 'landscape',
                    'size': 'medium'
                }
                
                response = requests.get(search_url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                videos = data.get('videos', [])
                
                if not videos:
                    logger.warning(f"No videos found for keyword: {keyword}")
                    continue
                
                
                for video in videos:
                    try:
                        video_id = video.get('id')
                        video_files = video.get('video_files', [])
                        
                        
                        suitable_file = None
                        for vf in video_files:
                            if vf.get('quality') in ['hd', 'sd'] and vf.get('file_type') == 'video/mp4':
                                suitable_file = vf
                                break
                        
                        if not suitable_file:
                            suitable_file = video_files[0] if video_files else None
                        
                        if not suitable_file:
                            continue
                        
                        
                        video_url = suitable_file.get('link')
                        if video_url:
                            local_path = download_video(video_url, keyword, session_id, i)
                            if local_path:
                                video_paths.append(local_path)
                                logger.info(f"Downloaded video for '{keyword}': {local_path}")
                                break
                                
                    except Exception as e:
                        logger.error(f"Error processing video for keyword '{keyword}': {str(e)}")
                        continue
                
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching videos for keyword '{keyword}': {str(e)}")
                continue
        
        
        if not video_paths:
            logger.warning("No videos downloaded from API, using fallback")
            return get_fallback_videos(keywords, session_id)
        
        return video_paths
        
    except Exception as e:
        logger.error(f"Video service error: {str(e)}")
        return get_fallback_videos(keywords, session_id)

def download_video(video_url: str, keyword: str, session_id: str, index: int) -> str:
    """
    Download a video from URL to local storage.
    
    Args:
        video_url (str): URL of the video to download
        keyword (str): Keyword associated with the video
        session_id (str): Session identifier
        index (int): Video index
        
    Returns:
        str: Local file path of downloaded video
    """
    try:
        
        safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_keyword}_{session_id}_{index}.mp4"
        filepath = os.path.join('static', 'videos', filename)
        
        
        logger.info(f"Downloading video from: {video_url}")
        response = requests.get(video_url, stream=True, timeout=60)
        response.raise_for_status()
        
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  
            logger.info(f"Successfully downloaded video: {filepath} ({os.path.getsize(filepath)} bytes)")
            return filepath
        else:
            logger.error(f"Downloaded file is empty or corrupted: {filepath}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return None
            
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return None

def get_fallback_videos(keywords: List[str], session_id: str) -> List[str]:
    """
    Create fallback placeholder videos when API fails.
    
    Args:
        keywords (List[str]): Keywords for video creation
        session_id (str): Session identifier
        
    Returns:
        List[str]: List of created placeholder video paths
    """
    try:
        from moviepy import ColorClip, TextClip, CompositeVideoClip
        
        video_paths = []
        
        for i, keyword in enumerate(keywords[:3]):
            try:
                
                duration = 5
                size = (1920, 1080)
                
                
                colors = ['blue', 'green', 'purple']
                color = colors[i % len(colors)]
                
                
                background = ColorClip(size=size, color=color, duration=duration)
                
                
                text = TextClip(
                    txt=f"{keyword.upper()}\nStock Video Placeholder",
                    fontsize=80,
                    color='white',
                    font='Arial',
                    size=size
                ).with_duration(duration).with_position('center')
                
                
                video = CompositeVideoClip([background, text])
                
                
                safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"fallback_{safe_keyword}_{session_id}_{i}.mp4"
                filepath = os.path.join('static', 'videos', filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                video.write_videofile(filepath, fps=24, verbose=False, logger=None)
                
                video_paths.append(filepath)
                logger.info(f"Created fallback video: {filepath}")
                
            except Exception as e:
                logger.error(f"Error creating fallback video for '{keyword}': {str(e)}")
                continue
        
        return video_paths
        
    except Exception as e:
        logger.error(f"Error creating fallback videos: {str(e)}")
        return []

def search_pexels_videos(keyword: str, per_page: int = 5) -> List[dict]:
    """
    Search for videos on Pexels.
    
    Args:
        keyword (str): Search keyword
        per_page (int): Number of results per page
        
    Returns:
        List[dict]: List of video data
    """
    try:
        pexels_api_key = os.getenv('PEXELS_API_KEY')
        if not pexels_api_key:
            return []
        
        headers = {'Authorization': pexels_api_key}
        url = "https://api.pexels.com/videos/search"
        
        params = {
            'query': keyword,
            'per_page': per_page,
            'orientation': 'landscape'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get('videos', [])
        
    except Exception as e:
        logger.error(f"Error searching Pexels videos: {str(e)}")
        return []

def test_video_service():
    
    try:
        test_keywords = ["technology", "business"]
        session_id = "test123"
        result = fetch_videos_from_keywords(test_keywords, session_id)
        print(f"Test successful: {len(result)} videos downloaded")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    
    test_video_service()