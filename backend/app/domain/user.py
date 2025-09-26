# backend/app/domain/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import ConfigDict 
# Properties that are shared by all User models
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Properties required to create a new user
class UserCreate(UserBase):
    password: str

# Properties to return to the client (never include the password!)
class UserDisplay(UserBase):
    id: int
    created_at: datetime

    # This is the new Pydantic V2 way to configure the model
    model_config = ConfigDict(from_attributes=True)