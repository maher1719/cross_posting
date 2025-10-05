# backend/app/tasks/ai_tasks.py

from app.core.celery_utils import celery_app
import requests
import json
import re

def call_ollama(prompt: str) -> str:
    """Helper function to call the Ollama service."""
    try:
        # --- FIX 1: Use the correct '/api/chat' endpoint ---
        ollama_url = "http://ollama:11434/api/generate"
        
        # --- FIX 2: The payload for the chat endpoint is different ---
        # It expects a list of "messages"
        payload = {
            "model": "qwen3:0.6", # Or your chosen model
            "messages": [
                {
                    "role": "user",# your own model name
                    "content": prompt
                }
            ],
            "stream": False # Keep this to get the full response at once
        }
        
        response = requests.post(ollama_url, data=json.dumps(payload), timeout=120)
        response.raise_for_status()
        response_data = response.json()
        
        # --- FIX 3: The response structure is also different ---
        # The content is inside response['message']['content']
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
        
        # TODO: Send a WebSocket event to the user to notify them.
        
        return cleaned_summary
    except Exception as e:
        print(f"Failed to generate summary for Post ID: {post_id}. Retrying... Error: {e}")
        raise self.retry(exc=e, max_retries=2, countdown=60)