from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2



class UserUpdateAdmin(BaseModel):
    role: Optional[str] = None  # "user" ou "admin"
    is_active: Optional[bool] = None
