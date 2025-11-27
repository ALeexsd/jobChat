from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.message import MessageType, MessageStatus


class MessageAttachmentCreate(BaseModel):
    file_name: str
    file_path: str
    file_type: str
    file_size: int


class MessageCreate(BaseModel):
    chat_id: int
    content: Optional[str] = None
    message_type: MessageType = MessageType.TEXT
    reply_to_id: Optional[int] = None
    attachment: Optional[MessageAttachmentCreate] = None


class MessageUpdate(BaseModel):
    content: str


class MessageReactionCreate(BaseModel):
    emoji: str


class MessageAttachmentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: Optional[str]
    message_type: MessageType
    status: MessageStatus
    reply_to_id: Optional[int]
    forwarded_from_id: Optional[int]
    is_edited: bool
    is_deleted: bool
    is_pinned: bool = False
    created_at: datetime
    attachments: List[MessageAttachmentResponse] = []

    class Config:
        from_attributes = True
