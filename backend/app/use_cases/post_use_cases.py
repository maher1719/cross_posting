# backend/app/use_cases/post_use_cases.py

from app.repositories.post_repository import PostRepository
from app.domain.post import PostCreate, PostDisplay, PostUpdate # --- ENHANCEMENT: Import PostUpdate ---
from app.tasks.posting_tasks import post_to_social_media
from uuid import uuid4

class PostUseCases:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_all_posts(self) -> list[PostDisplay]:
        post_models = self.post_repo.get_all()
        return [PostDisplay.from_orm(post) for post in post_models]

    def create_post(self, post_create: PostCreate) -> PostDisplay:
        post_model = self.post_repo.add(post_create)
        print(f"Delegating post creation for Post ID: {post_model.id} to Celery.")
        post_to_social_media.delay(post_model.id, post_model.content)
        return PostDisplay.from_orm(post_model)

    def get_by_id(self, post_id: uuid4) -> PostDisplay | None:
        post_model = self.post_repo.get_by_id(post_id)
        return PostDisplay.from_orm(post_model) if post_model else None

    def delete_by_id(self, post_id: uuid4) -> bool:
        return self.post_repo.delete_by_id(post_id)
    
    def delete_by_user_id(self, user_id: uuid4) -> uuid4:
        return self.post_repo.delete_by_user_id(user_id)
    
    def update(self, post_update: PostUpdate) -> PostDisplay | None:
        # --- ENHANCEMENT: Pass the Pydantic object down and return a display model ---
        updated_post_model = self.post_repo.update(post_update) 
        return PostDisplay.from_orm(updated_post_model) if updated_post_model else None

post_repository.create(obj_in=my_post_create_schema)