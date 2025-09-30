# backend/app/use_cases/post_use_cases.py

from app.helpers.crud import CRUDUseCases
from app.repositories.post_repository import post_repository, PostRepository
from app.domain.post import PostCreate, PostUpdate, PostDisplay
from app.tasks.posting_tasks import post_to_social_media
from uuid import uuid4

# --- 1. Inherit from the generic CRUDUseCases ---
class PostUseCases(CRUDUseCases[PostRepository, PostCreate, PostUpdate, PostDisplay]):
    def __init__(self, repository: PostRepository):
        super().__init__(repository)

    # --- 2. OVERRIDE the 'create' method to add your specific business logic ---
    def create(self, *, obj_in: PostCreate) -> PostDisplay:
        # First, call the base 'create' method to save the post to the DB
        new_post_display = super().create(obj_in=obj_in)
        
        # Now, add your unique business logic for posts
        print(f"Delegating post creation for Post ID: {new_post_display.id} to Celery.")
        post_to_social_media.delay(new_post_display.id, new_post_display.content)
        
        return new_post_display

    # --- 3. Add any custom methods that are NOT standard CRUD ---
    def delete_posts_by_user(self, user_id: uuid4) -> int:
        # This is a custom method, so we add it here.
        # It assumes you'd add a `delete_by_user_id` method to your repository.
        return self.repository.delete_by_user_id(user_id=user_id)
        

# --- 4. Export a single, ready-to-use instance ---
post_use_cases = PostUseCases(post_repository)
