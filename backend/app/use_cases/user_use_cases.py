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
        Handles the core business logic of user authentication.
        It finds a user and verifies their password.
        Returns the full SQLAlchemy User model on success, or None on failure.
        """
        # 1. Get the user from the database via the repository
        user_model = self.user_repo.get_by_email(user_login.email)
        if not user_model:
            return None # User does not exist

        # 2. THE FIX: Call pwd_context.verify() with the PLAIN TEXT password
        #    from the login form and the HASHED password from the database.
        if not pwd_context.verify(user_login.password, user_model.hashed_password):
            return None # Passwords do not match
            
        # 3. If both checks pass, success! Return the full user object.
        return user_model
