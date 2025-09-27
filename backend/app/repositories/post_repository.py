# NEW, CORRECTED VERSION
from app.models.post_model import Post
from app.domain.post import PostCreate
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
