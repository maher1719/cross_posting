
from passlib.context import CryptContext
from app.models.user_model import User
from app.domain.user import UserCreate, UserLogin
from app.core.db import db

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


#TODO fix to return error invalid
    def login_user(self, user_login: UserLogin, hashed_passowrd:str) -> User | None:
        user = self.get_by_email(user_login.email)
        if not user:
            return {"error": "Invalid email or password"}
        print(user)
        if user and pwd_context.verify(hashed_passowrd, user.hashed_password):
            return user
        return {"error": "Invalid email or password"}