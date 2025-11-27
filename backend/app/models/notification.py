from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class NotificationType(str, enum.Enum):
    MESSAGE = "message"
    TASK_ASSIGNED = "task_assigned"
    TASK_COMMENT = "task_comment"
    TASK_STATUS_CHANGED = "task_status_changed"
    ROUTE_ASSIGNED = "route_assigned"
    VACATION_REQUEST = "vacation_request"
    BIRTHDAY = "birthday"
    MENTION = "mention"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    link = Column(String, nullable=True)  # URL для перехода
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
