# backend/app/use_cases/post_use_cases.py

from app.helpers.crud.crud_use_cases import CRUDUseCases
from app.repositories.post_repository import post_repository, PostRepository
from app.domain.post import PostCreate, PostUpdate, PostDisplay
from app.tasks.posting_tasks import post_to_social_media
from app.tasks.ai_tasks import generate_twitter_summary
from uuid import uuid4


# --- 1. Inherit from the generic CRUDUseCases ---
class PostUseCases(CRUDUseCases[PostRepository, PostCreate, PostUpdate, PostDisplay]):
    def __init__(self, repository: PostRepository):
        # Pass the repository AND the display schema to the parent class
        super().__init__(repository, display_schema=PostDisplay)

    # --- 2. OVERRIDE the 'create' method to add your specific business logic ---
    def create(self, *, obj_in: PostCreate) -> PostDisplay:
        # 1. Call the base 'create' method to synchronously save the post to the DB.
        db_obj = self.repository.create(obj_in=obj_in)
        
        # 2. Check the flag from the API payload.
        if obj_in.generate_for_twitter:
            print(f"Orchestrating AI summary for Post ID: {db_obj.id}")
            # 3. Asynchronously delegate the slow AI work to Celery.
            generate_twitter_summary.delay(str(db_obj.id), db_obj.content_text)
        
        # 4. Immediately return the newly created post data to the user.
        return PostDisplay.from_orm(db_obj)

    # --- 3. Add any custom methods that are NOT standard CRUD ---
    def delete_posts_by_user(self, user_id: uuid4) -> int:
        # This is a custom method, so we add it here.
        # It assumes you'd add a `delete_by_user_id` method to your repository.
        # return self.repository.delete_by_user_id(user_id=user_id)
        pass  # Placeholder for now


# --- 4. Export a single, ready-to-use instance ---
post_use_cases = PostUseCases(post_repository)
