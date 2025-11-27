from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ChatType(str, enum.Enum):
    PRIVATE = "private"
    GROUP = "group"


class ChatMemberRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # Для групповых чатов
    chat_type = Column(SQLEnum(ChatType), nullable=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    members = relationship("ChatMember", back_populates="chat", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(ChatMemberRole), default=ChatMemberRole.MEMBER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_read_message_id = Column(Integer, nullable=True)
    # last_read_at = Column(DateTime(timezone=True), nullable=True)  # Временно отключено

    chat = relationship("Chat", back_populates="members")
