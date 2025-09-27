from app.repositories.post_repository import PostRepository
from app.domain.post import PostCreate, PostDisplay
from app.models.post_model import Post
from app.tasks.posting_tasks import post_to_social_media


class PostUseCases:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_all_posts(self) -> list[PostDisplay]:
         post_models = self.post_repo.get_all()
        # Convert SQLAlchemy models to Pydantic models for the API layer
         return [PostDisplay.from_orm(post) for post in post_models]



    def create_post(self, post_create: PostCreate) -> Post:
        post_model = self.post_repo.add(post_create)
        # Convert the new SQLAlchemy model to a Pydantic model
        # Step 2: Delegate the slow work to our background task.
        # We call '.delay()' to tell Celery to run this in the background.
        print(f"Delegating post creation for Post ID: {post_model.id} to Celery.")
        post_to_social_media.delay(post_model.id, post_model.content)
        
        # Step 3: Immediately return a response to the user.
        # The user does not have to wait for the 15-second process to finish.
        return PostDisplay.from_orm(post_model)



    def get_by_id(self, post_id: int) -> PostDisplay | None:
        post_model = self.post_repo.get_by_id(post_id)
        if post_model:
            return PostDisplay.from_orm(post_model)
        else:
            return None
    def delete_by_id(self, post_id: int) -> bool:
        return self.post_repo.delete_post_by_id(post_id)
    
    def delete_by_user_id(self, user_id: int) -> bool:
        return self.post_repo.delete_by_user_id(user_id)
    
    def update(self, id: int, content: str) -> bool:
        post_model = self.post_repo.update(id, content) 
        return post_model
        


    