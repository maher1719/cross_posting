# backend/app/tasks/posting_tasks.py

from app.core.celery_utils import celery_app  # Import our celery instance
import time
from uuid import uuid4


@celery_app.task
def post_to_social_media(post_id: uuid4, content: str):
    """
    This is our main posting service task.
    It takes a post ID and its content and sends it to various platforms.
    """
    print(f"--- Starting social media post for Post ID: {post_id} ---")
    print(f"Content: {content}")

    try:
        # 1. Load credentials securely from environment variables
        api_key = os.environ.get("X_API_KEY")
        api_secret = os.environ.get("X_API_SECRET")
        access_token = os.environ.get("X_ACCESS_TOKEN")
        access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

        if not all([api_key, api_secret, access_token, access_token_secret]):
            print("!!! ERROR: Missing X API credentials in .env file.")
            raise ValueError("Missing X API credentials.")

        # 2. Authenticate with the X API using tweepy
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        # 3. Post the tweet!
        print("Posting to X (Twitter)...")
        response = client.create_tweet(text=content)
        print("...X post successful! Tweet ID:", response.data["id"])

        # --- (In the future, you could add other platforms here) ---

        print(f"--- Finished social media post for Post ID: {post_id} ---")
        return f"Successfully posted to X for Post ID: {post_id}"

    except Exception as e:
        # If the API call fails (e.g., network error, duplicate tweet),
        # Celery can automatically retry the task.
        print(f"!!! ERROR posting for Post ID: {post_id} - {e}")
        # Retry the task after 5 minutes, up to 3 times.
        raise self.retry(exc=e, countdown=300, max_retries=3)

    try:
        # --- This is where the real logic will go ---

        # 2. Post to Facebook (Simulated)
        print("Posting to Facebook...")
        time.sleep(5)  # Simulate another slow API call
        print("...Facebook post successful!")

        # 3. Post to LinkedIn (Simulated)
        print("Posting to LinkedIn...")
        time.sleep(5)  # Simulate another slow API call
        print("...LinkedIn post successful!")

        # 4. Update our database to mark the post as "published"
        # (We would need a repository method for this)
        print(f"--- Finished social media post for Post ID: {post_id} ---")

        return f"Successfully posted to 3 platforms for Post ID: {post_id}"

    except Exception as e:
        # If any of the API calls fail, the task can be retried or marked as failed.
        print(f"!!! ERROR posting for Post ID: {post_id} - {e}")
        # Celery has built-in retry mechanisms we can use here.
        raise
