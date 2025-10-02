
from app.core.celery_utils import celery_app
import tweepy
import requests
import os

@celery_app.task(bind=True)
def post_to_social_media(self, post_id: int, content: str):
    """
    This task takes a post's content and publishes it to X (Twitter)
    using the modern OAuth 2.0 Bearer Token flow.
    """
    print(f"--- Starting REAL social media post for Post ID: {post_id} ---")
    print(f"Content: {content}")

    try:

        api_key = os.environ.get('X_API_KEY')
        api_secret = os.environ.get('X_API_SECRET')
        access_token = os.environ.get('X_ACCESS_TOKEN')
        access_token_secret = os.environ.get('X_ACCESS_TOKEN_SECRET')

        if not all([api_key, api_secret, access_token, access_token_secret]):
            print("!!! ERROR: Missing X API credentials in .env file.")
            raise ValueError("Missing X API credentials.")

        bearer_token = os.environ.get('X_BEARER_TOKEN')
        if not bearer_token:
            print("!!! ERROR: Missing X_BEARER_TOKEN in .env file.")
            raise ValueError("Missing X Bearer Token.")

        client = tweepy.Client(bearer_token=bearer_token, 
        consumer_key=api_key, 
        consumer_secret=api_secret, 
        access_token=access_token, 
        access_token_secret=access_token_secret)
        

        


        # 3. Post the tweet!
        print("Posting to X (Twitter)...")
        #response = requests.post(url, json=payload, headers=headers)
        response = client.create_tweet(text=content)
        print("gemini response"+ respone.data)
        print("...X post successful! Tweet ID:", response)

        print(f"--- Finished social media post for Post ID: {post_id} ---")
        return f"Successfully posted to X for Post ID: {post_id}"

    except Exception as e:
        print(f"!!! ERROR posting for Post ID: {post_id} - {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)