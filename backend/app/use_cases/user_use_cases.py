# backend/app/use_cases/user_use_cases.py

from passlib.context import CryptContext
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.domain.user import UserCreate, UserDisplay, UserLogin

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_new_user(self, user_create: UserCreate) -> UserDisplay:
        # Business Rule: Check if user already exists
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise ValueError(
                "Email already registered"
            )  # We'll handle this in the API layer

        # Hash the password
        hashed_password = pwd_context.hash(user_create.password)

        # Create the user via the repository
        new_user_model = self.user_repo.add(user_create, hashed_password)

        # Convert the SQLAlchemy model to a Pydantic display model
        return UserDisplay.from_orm(new_user_model)

    def login_user(self, user_login: UserLogin) -> User | None:
        """
        Handles the core logic of user authentication.
        Returns the User model on success, None on failure.
        """
        user_model = self.user_repo.get_by_email(user_login.email)
        if not user_model:
            return None
        passowrd_hashed = pwd_context.hash(user_login.password)
        if not pwd_context.verify(passowrd_hashed, user_model.hashed_password):
            return None

        return user_model
