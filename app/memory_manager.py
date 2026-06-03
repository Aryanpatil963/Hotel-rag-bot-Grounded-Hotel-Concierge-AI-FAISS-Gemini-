import os
import json
import google.generativeai as genai
from collections import defaultdict

# Configure API Key
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
is_valid_key = api_key and api_key != "your_api_key_here"
if is_valid_key:
    genai.configure(api_key=api_key)

# Simple in-memory session history: session_id -> list of {"user": str, "bot": str}
# Limit size to 5 turns
session_store = defaultdict(list)

def add_turn_to_memory(session_id: str, user_query: str, bot_response: str):
    history = session_store[session_id]
    history.append({"user": user_query, "bot": bot_response})
    if len(history) > 5:
        history.pop(0)

def get_session_history(session_id: str):
    return session_store[session_id]

import time
import random

def call_gemini_with_retry(model, prompt, max_retries=3, initial_delay=1.0):
    """Executes a Gemini API call with exponential backoff and jitter."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"[Gemini API Retry] Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay + random.uniform(0.0, 0.5))
            delay *= 2

def resolve_pronouns(session_id: str, query: str) -> str:
    """
    Resolves pronouns or contextual references in the query using the session's chat history.
    Example: "What time does it close?" -> "What time does the swimming pool close?"
    """
    if not is_valid_key:
        return query

    history = session_store[session_id]
    if not history:
        return query

    # Formulate a history string
    history_str = ""
    for idx, turn in enumerate(history):
        history_str += f"Guest: {turn['user']}\nConcierge: {turn['bot']}\n"

    prompt = f"""
    You are an assistant that resolves pronouns and context references in user queries.
    Analyze the conversation history and the latest user query, then rewrite the query to be completely self-contained and search-friendly (specifically for standard keyword or vector semantic search).
    
    Rules:
    1. Identify pronouns like "it", "they", "there", "its", "them" or contextual phrases in the latest query.
    2. Replace them with the actual entities they refer to from the conversation history.
    3. If the latest query does not contain any pronouns and is already complete and self-contained, return the latest query EXACTLY as is.
    4. Keep the rewritten query concise, natural, and search-friendly.
    
    Conversation History:
    {history_str}
    
    Latest Query:
    "{query}"
    
    Return ONLY the rewritten search query. Do not include explanations, quotes, or JSON formatting.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = call_gemini_with_retry(model, prompt)
        rewritten = response.text.strip()
        print(f"[Memory Manager] Resolved query '{query}' -> '{rewritten}'")
        return rewritten
    except Exception as e:
        print(f"Error in memory manager pronoun resolution: {e}")
        return query
