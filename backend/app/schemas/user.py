from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional
from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    birth_date: Optional[date] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[UserStatus] = None


class UserResponse(UserBase):
    id: int
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole
    status: UserStatus
    avatar_url: Optional[str] = None
    last_seen: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    username: str
    password: str
