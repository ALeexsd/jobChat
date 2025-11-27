from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.chat import ChatType, ChatMemberRole


class ChatCreate(BaseModel):
    name: Optional[str] = None
    chat_type: ChatType
    member_ids: List[int]  # Список ID участников


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class ChatMemberResponse(BaseModel):
    id: int
    user_id: int
    role: ChatMemberRole
    joined_at: datetime

    class Config:
        from_attributes = True


class LastMessageResponse(BaseModel):
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: int
    name: Optional[str]
    chat_type: ChatType
    avatar_url: Optional[str]
    created_at: datetime
    members: List[ChatMemberResponse] = []
    last_message: Optional[LastMessageResponse] = None

    class Config:
        from_attributes = True
