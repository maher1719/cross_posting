# backend/app/repositories/post_repository.py

from app.models.post_model import Post
from app.domain.post import PostCreate, PostUpdate # --- ENHANCEMENT: Import PostUpdate ---
from app.core.db import db

class PostRepository:
    def get_all(self) -> list[Post]:
        return Post.query.all()

    def add(self, post_create: PostCreate) -> Post:
        new_post = Post(
            content=post_create.content,
            user_id=post_create.user_id
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def get_by_id(self, post_id: int) -> Post | None:
        return db.session.get(Post, post_id)
    
    def delete_by_id(self, post_id: int) -> bool:
        post = self.get_by_id(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        return False
    
    def delete_by_user_id(self, user_id: int) -> int:
        # --- ENHANCEMENT: This method is more powerful if it returns how many posts were deleted ---
        num_deleted = Post.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return num_deleted

    def update(self, post_update: PostUpdate) -> Post | None:
        # --- ENHANCEMENT: Accept the Pydantic model directly for consistency ---
        post = self.get_by_id(post_update.id)
        if post:
            post.content = post_update.content
            db.session.commit()
            return post
        return None