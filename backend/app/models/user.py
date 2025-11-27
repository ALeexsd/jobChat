from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    position = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    status = Column(SQLEnum(UserStatus), default=UserStatus.OFFLINE, nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
