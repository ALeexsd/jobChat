from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # personal, work, etc.
    is_pinned = Column(Boolean, default=False)
    about_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # Заметка о пользователе
    tags = Column(String, nullable=True)  # Comma-separated tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
