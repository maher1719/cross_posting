# backend/app/domain/post.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import uuid4
from pydantic import UUID4

# --- A base model for any entity that has a UUID ---
class UUIDModel(BaseModel):
    id: UUID4

# --- Base properties for a post ---
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, description="The content of the post.")

# --- DTO for creating a new post ---
class PostCreate(PostBase):
    user_id: UUID4

# --- DTO for updating a post ---
class PostUpdate(PostBase):
    pass # For a PATCH, we only need the content. The ID comes from the URL.

# --- DTO for displaying a post to the client ---
class PostDisplay(UUIDModel, PostBase):
    user_id: UUID4
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)