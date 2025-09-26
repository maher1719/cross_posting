# NEW, CORRECTED VERSION
from app.models.user_model import User
from app.domain.user import UserCreate
from app.core.db import db

class UserRepository:
    def add(self, user_create: UserCreate, hashed_password: str) -> User:
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        db.session.add(new_user)
        # We will let the Flask-SQLAlchemy extension manage the commit.
        # Often, it's better to commit at the end of the request.
        # For simplicity now, we will commit here.
        db.session.commit()
        # The refresh is not necessary for returning the object.
        return new_user

    def get_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()