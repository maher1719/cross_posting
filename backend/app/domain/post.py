# backend/app/domain/post.py

from pydantic import BaseModel, ConfigDict, Field
from uuid import uuid4
from datetime import datetime

# --- ENHANCEMENT: Added a base class for models that have an ID ---
class PostId(BaseModel):
    id: uuid4 
# --- Properties that are shared by all Post models ---
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, description="The content of the post")

# --- Data required to create a new post ---
class PostCreate(PostBase):
    user_id: uuid4 

# --- Data structure for updating an existing post ---
class PostUpdate(PostId, PostBase):
    # This class now inherits both 'id' and 'content'
    pass

# --- Data structure for returning a post to the client ---
class PostDisplay(PostId, PostCreate):
    # Inherits id, content, and user_id
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)