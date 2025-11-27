from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: bool = False
    about_user_id: Optional[int] = None
    tags: Optional[str] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = None
    tags: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str]
    category: Optional[str]
    is_pinned: bool
    about_user_id: Optional[int]
    tags: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
