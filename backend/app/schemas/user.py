# app/schemas/user.py
from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    email: EmailStr
    name: str | None = None
    company: str | None = None
class UserUpdate(BaseModel):
    name: str | None = None
    company: str | None = None
class UserOut(UserCreate):
    id: int

    model_config = {"from_attributes": True}  

