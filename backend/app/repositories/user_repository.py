
from passlib.context import CryptContext
from app.models.user_model import User
from app.domain.user import UserCreate, UserLogin
from app.core.db import db
from uuid import uuid4

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


    def get_by_id(self, user_id: uuid4) -> User | None:
        return db.session.get(User, user_id)