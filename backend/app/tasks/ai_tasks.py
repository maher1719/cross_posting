# backend/app/tasks/ai_tasks.py

from app.core.celery_utils import celery_app
from app.tasks.posting_tasks import post_to_social_media
import requests
import json
import re


def call_ollama(prompt: str) -> str:
    """Helper function to call the Ollama service using the chat endpoint."""
    try:
        # --- CHANGE 1: THE URL PATH MUST BE '/api/chat' ---
        ollama_url = "http://ollama:11434/api/chat"
        
        # --- CHANGE 2: THE PAYLOAD MUST USE THE 'messages' STRUCTURE ---
        payload = {
            "model": "qwen3:0.6b",
            "messages": [
                { "role": "user", "content": prompt }
            ],
            "stream": False
        }
        
        response = requests.post(ollama_url, data=json.dumps(payload), timeout=300)
        response.raise_for_status()
        response_data = response.json()
        
        # --- CHANGE 3: THE RESPONSE MUST BE PARSED FROM the 'message' object ---
        return response_data.get('message', {}).get('content', '')

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        raise

def clean_llm_output(text: str) -> str:
    """Helper function to clean up common LLM artifacts."""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return text.strip()

@celery_app.task(bind=True)
def generate_twitter_summary(self, post_id: str, content_text: str):
    try:
        print(f"Starting AI summary for Post ID: {post_id}")
        
        prompt = f"Summarize the following text into a concise tweet (max 280 characters) and add 3-5 relevant hashtags at the end.\n\nTEXT:\n---\n{content_text}\n---"
        
        raw_summary = call_ollama(prompt)
        cleaned_summary = clean_llm_output(raw_summary)
        
        # TODO: Save the cleaned_summary to the 'AdaptedPosts' database table
        print(f"Successfully generated summary for Post ID: {post_id}: '{cleaned_summary}'")
        
        # --- 2. THIS IS THE FINAL STEP: CHAIN THE NEXT TASK ---
        # Instead of just returning, we will now call the next task in the chain.
        print(f"Now, delegating the generated summary to the Twitter posting task...")
        post_to_social_media.delay(post_id, cleaned_summary)
        
        
        return cleaned_summary
    except Exception as e:
        print(f"Failed to generate summary for Post ID: {post_id}. Retrying... Error: {e}")
        raise self.retry(exc=e, max_retries=2, countdown=60)
    