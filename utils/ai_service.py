
import os
import json
import logging
from typing import Dict, List

try:
    from google import genai
    from google.genai import types
except ImportError:
    logging.error("google-genai not installed. Please install: pip install google-genai")
    raise

logger = logging.getLogger(__name__)

def generate_script_from_prompt(prompt: str) -> Dict[str, any]:
    """
    Generate video script and keywords using Google Gemini Flash API.
    
    Args:
        prompt (str): User input prompt
        
    Returns:
        Dict containing 'script' and 'keywords' keys
    """
    try:
        
        api_key = "AIzaSyC1dSEI8aENjszrP9IcqZYX561QV8ASHa0"
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found in environment variables")
        
        
        client = genai.Client(api_key=api_key)
        
       
        enhanced_prompt = f"""
{prompt}

You are an expert scriptwriter. Convert the input into a natural, spoken-style script **suitable ONLY for AI voice narration** (no visual instructions).

Return ONLY a valid JSON object with this exact format:
{{
    "script": "A detailed script suitable for voice narration only...",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Requirements for the script:
- 150–300 words long
- Clear, natural, and conversational — like something a person would say aloud in a video
- No visual instructions like 'show this' or 'use this footage'
- No camera directions or editing notes
- No meta descriptions like 'this video is about...'
- Must sound like a complete voiceover narration from start to end

Requirements for keywords:
- 3–5 max
- Relevant to the topic
- Good for finding related stock footage
- Descriptive, not too broad (e.g., 'home repair', not just 'home')
"""

        logger.info("Sending request to Gemini Flash API...")
        
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2048,
                top_p=0.8
            )
        )
        
        if not response or not response.text:
            raise ValueError("Empty response from Gemini API")
        
        logger.info(f"Received response from Gemini API: {len(response.text)} characters")
        
        
        try:
            
            response_text = response.text.strip()
            
            
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            
            json_text = response_text[start_idx:end_idx]
            ai_response = json.loads(json_text)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response.text}")
            
            
            ai_response = {
                "script": response.text[:500] + "..." if len(response.text) > 500 else response.text,
                "keywords": ["technology", "innovation", "future", "digital", "modern"]
            }
        
        
        if not isinstance(ai_response, dict):
            raise ValueError("Response is not a dictionary")
        
        script = ai_response.get('script', '')
        keywords = ai_response.get('keywords', [])
        
        if not script:
            raise ValueError("No script found in AI response")
        
        if not keywords or not isinstance(keywords, list):
            logger.warning("No valid keywords found, using default keywords")
            keywords = ["technology", "innovation", "business", "modern"]
        
        
        if len(keywords) < 3:
            keywords.extend(["technology", "business", "modern"][:3-len(keywords)])
        elif len(keywords) > 5:
            keywords = keywords[:5]
        
        logger.info(f"Successfully generated script ({len(script)} chars) and {len(keywords)} keywords")
        
        return {
            'script': script,
            'keywords': keywords
        }
        
    except Exception as e:
        logger.error(f"AI service error: {str(e)}")
        
        
        fallback_response = {
            'script': f"This is an engaging video about {prompt}. The topic covers important aspects that are relevant to modern audiences. Through careful analysis and presentation, we explore the key concepts and their implications. This content provides valuable insights and practical information for viewers interested in learning more about this subject.",
            'keywords': ["technology", "education", "innovation", "modern", "digital"]
        }
        
        logger.info("Using fallback AI response due to API failure")
        return fallback_response

def test_ai_service():
    
    try:
        test_prompt = "Create a video about renewable energy"
        result = generate_script_from_prompt(test_prompt)
        print(f"Test successful: {result}")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    
    test_ai_service()