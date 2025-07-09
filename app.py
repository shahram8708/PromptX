
import os
import logging
import shutil
import json
import time
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, url_for, send_file, flash, redirect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


load_dotenv()


from utils.ai_service import generate_script_from_prompt
from utils.video_service import fetch_videos_from_keywords
from utils.tts_service import generate_voiceover_from_script
from utils.video_processor import merge_video_audio_captions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  


UPLOAD_FOLDERS = {
    'videos': 'static/videos',
    'audio': 'static/audio', 
    'final': 'static/final',
    'logs': 'logs'
}

for folder in UPLOAD_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    
    try:
        
        prompt = request.form.get('prompt', '').strip()
        logger.info(f"[DEBUG] Incoming form data: {dict(request.form)}")
        logger.info(f"[DEBUG] Extracted prompt: '{prompt}'")
        if not prompt:
            flash('Please enter a valid prompt.', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Starting video generation for prompt: {prompt[:100]}...")
        
        
        session_id = str(uuid.uuid4())[:8]
        
        
        logger.info("Step 1: Generating script from AI...")
        try:
            ai_response = generate_script_from_prompt(prompt)
            script = ai_response.get('script', '')
            keywords = ai_response.get('keywords', [])
            
            if not script or not keywords:
                raise ValueError("AI response missing script or keywords")
                
            logger.info(f"Generated script ({len(script)} chars) and keywords: {keywords}")
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            flash('AI script generation failed. Please try again.', 'error')
            return redirect(url_for('index'))
        
        
        logger.info("Step 2: Fetching stock videos...")
        try:
            video_paths = fetch_videos_from_keywords(keywords, session_id)
            if not video_paths:
                raise ValueError("No videos found for keywords")
            logger.info(f"Downloaded {len(video_paths)} videos: {video_paths}")
        except Exception as e:
            logger.error(f"Video fetching failed: {str(e)}")
            flash('Stock video fetching failed. Please try again.', 'error')
            return redirect(url_for('index'))
        
        
        logger.info("Step 3: Generating voiceover...")
        try:
            audio_path = generate_voiceover_from_script(script, session_id)
            if not audio_path or not os.path.exists(audio_path):
                raise ValueError("Audio generation failed")
            logger.info(f"Generated audio: {audio_path}")
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            flash('Voice generation failed. Please try again.', 'error')
            return redirect(url_for('index'))
        
        
        logger.info("Step 4: Merging final video...")
        try:
            final_video_path = merge_video_audio_captions(
                video_paths, audio_path, script, session_id
            )
            if not final_video_path or not os.path.exists(final_video_path):
                raise ValueError("Video merging failed")
            logger.info(f"Generated final video: {final_video_path}")
        except Exception as e:
            logger.error(f"Video merging failed: {str(e)}")
            flash('Video merging failed. Please try again.', 'error')
            return redirect(url_for('index'))
        
        
        cleanup_temp_files(session_id, keep_final=True)
        
        logger.info(f"Video generation completed successfully: {final_video_path}")
        
        
        return render_template('result.html', 
                             video_path=final_video_path,
                             script=script,
                             keywords=keywords,
                             original_prompt=prompt)
                             
    except Exception as e:
        logger.error(f"Unexpected error in video generation: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_file(filename):
    
    try:
        file_path = os.path.join('static', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        flash('Download failed.', 'error')
        return redirect(url_for('index'))

@app.route('/status/<session_id>')
def get_status(session_id):
    
    
    return jsonify({'status': 'processing', 'message': 'Generating video...'})

@app.errorhandler(413)
def request_entity_too_large(error):
    
    flash('File too large. Maximum size is 100MB.', 'error')
    return render_template('error.html', error_message='File too large'), 413

@app.errorhandler(500)
def internal_server_error(error):
    
    logger.error(f"Internal server error: {str(error)}")
    return render_template('error.html', error_message='Internal server error'), 500

def cleanup_temp_files(session_id, keep_final=False):
    
    try:
        
        video_dir = Path(UPLOAD_FOLDERS['videos'])
        for video_file in video_dir.glob(f"*{session_id}*"):
            video_file.unlink(missing_ok=True)
            
        
        audio_dir = Path(UPLOAD_FOLDERS['audio'])
        for audio_file in audio_dir.glob(f"*{session_id}*"):
            audio_file.unlink(missing_ok=True)
            
        
        if not keep_final:
            final_dir = Path(UPLOAD_FOLDERS['final'])
            for final_file in final_dir.glob(f"*{session_id}*"):
                final_file.unlink(missing_ok=True)
                
        logger.info(f"Cleaned up temporary files for session {session_id}")
    except Exception as e:
        logger.warning(f"Cleanup failed for session {session_id}: {str(e)}")

def retry_operation(operation, max_retries=2, delay=1):
    
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries:
                raise e
            logger.warning(f"Operation failed (attempt {attempt + 1}), retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2

if __name__ == '__main__':
    logger.info("Starting AI Video Generator Flask Application")
    app.run(debug=True, host='0.0.0.0', port=5000)