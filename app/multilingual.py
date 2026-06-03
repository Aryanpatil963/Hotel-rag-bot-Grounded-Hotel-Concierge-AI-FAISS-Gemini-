import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
is_valid_key = api_key and api_key != "your_api_key_here"
if is_valid_key:
    genai.configure(api_key=api_key)

def get_gemini_client():
    if not is_valid_key:
        return None
    return genai.GenerativeModel("gemini-2.0-flash")

import time
import random

def call_gemini_with_retry(model, prompt, generation_config=None, max_retries=3, initial_delay=1.0):
    """Executes a Gemini API call with exponential backoff and jitter."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt, generation_config=generation_config)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"[Gemini API Retry] Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay + random.uniform(0.0, 0.5))
            delay *= 2

def detect_and_translate(query: str):
    """
    Detects if the query is in English, Hindi, or Hinglish.
    If it is Hindi or Hinglish, translates it to English.
    Returns: (detected_language, translated_query)
    """
    # Clean check
    if not query or query.strip() == "":
        return "en", ""
        
    if not is_valid_key:
        return "en", query

    prompt = f"""
    Analyze the following user query sent to a hotel concierge bot:
    "{query}"

    1. Classify the language as exactly one of: "en", "hi", "hinglish".
       - "en" is English.
       - "hi" is Hindi (in Devanagari script, e.g., क्या स्विमिंग पूल खुला है?).
       - "hinglish" is Hindi written in the Latin alphabet or blended with English (e.g., "wifi code kya hai?", "swimming pool kab close hota hai?").
    2. Provide the translation of this query into plain English. If the language is already "en", the translation should be identical to the query.

    Return ONLY a JSON object with this exact structure:
    {{
      "detected_language": "en" | "hi" | "hinglish",
      "translated_query": "translated string"
    }}
    """
    
    try:
        model = get_gemini_client()
        response = call_gemini_with_retry(
            model,
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text.strip())
        return data.get("detected_language", "en"), data.get("translated_query", query)
    except Exception as e:
        print(f"Error in multilingual detect_and_translate: {e}")
        # Default fallback
        return "en", query

def translate_to_target(text: str, target_lang: str) -> str:
    """
    Translates English text back into the target language (hi or hinglish).
    If target_lang is 'en', returns text as is.
    """
    if target_lang == "en" or not text or not is_valid_key:
        return text

    prompt = f"""
    You are a luxury hotel concierge translating responses for a guest.
    Translate the following English response into {target_lang.upper()}.
    
    Target languages guide:
    - "hi": Use natural, polite Hindi (Devanagari script) suitable for a 5-star hotel concierge.
    - "hinglish": Use natural, conversational Hinglish (Hindi written in Roman script, e.g., "Aapka room level 12 par hai aur pool 10:00 PM tak open hai."). Keep standard English terms like "pool", "WiFi", "room" as is, just write the sentence structure in Hinglish.
    
    Source English response:
    "{text}"

    Return ONLY the translated text. Do not include quotes, explanations, or JSON formatting.
    """
    
    try:
        model = get_gemini_client()
        response = call_gemini_with_retry(model, prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in translating response to {target_lang}: {e}")
        return text
