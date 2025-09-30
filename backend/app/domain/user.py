# backend/app/domain/user.py

from pydantic import BaseModel, EmailStr, ConfigDict, Field
import uuid
from datetime import datetime

# --- Base properties shared across User models ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, description="The user's unique username.")
    email: EmailStr

# --- DTO for creating a new user ---
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password (min 8 characters).")

# --- DTO for user login ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- DTO for displaying user data to the client (NEVER includes password) ---
class UserDisplay(UserBase):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- DTO for the JWT Token response ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"