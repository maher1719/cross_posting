from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict 
# Properties that are shared by all Post models
class PostBase(BaseModel):
    content: str
    
class PostCreate(PostBase):
    user_id: int

class PostDisplay(PostBase):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
class PostUpdate(PostBase):
    id: int


class PostDelete(BaseModel):
    id: int

class PostUsetDelete(BaseModel):
    user_id: int
