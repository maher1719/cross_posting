# backend/app/repositories/post_repository.py

from app.helpers.crud.crud_db import CRUDBase
from app.models.post_model import Post
from app.domain.post import PostCreate, PostUpdate
from app.core.db import db
from uuid import uuid4

# --------------------------------------------------------------------------
# 1. DEFINE THE SPECIFIC POST REPOSITORY CLASS
# --------------------------------------------------------------------------
# This class inherits all the generic CRUD functionality (get, get_all, 
# create, update, delete) from CRUDBase.
# We "tighten the connection" by telling it the specific SQLAlchemy model
# and Pydantic schemas it will work with.
class PostRepository(CRUDBase[Post, PostCreate, PostUpdate]):
    def __init__(self):
        """
        Initializes the PostRepository by telling the base class
        which SQLAlchemy model to use (the 'Post' model).
        """
        super().__init__(Post)

    # --------------------------------------------------------------------------
    # 2. ADD CUSTOM, POST-SPECIFIC DATABASE METHODS HERE
    # --------------------------------------------------------------------------
    # The CRUDBase handles the simple cases. Any complex, entity-specific
    # database query logic belongs here.
    
    def delete_by_user_id(self, user_id: uuid4) -> int:
        """
        Deletes all posts belonging to a specific user in a single,
        efficient database operation.

        Returns:
            int: The number of posts that were deleted.
        """
        num_deleted = self.model.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return num_deleted

# --------------------------------------------------------------------------
# 3. CREATE AND EXPORT A SINGLETON INSTANCE
# --------------------------------------------------------------------------
# By creating a single instance of the repository here, we ensure that
# the entire application uses the same object, which is efficient and
# prevents potential state issues.
post_repository = PostRepository()