from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Enum as SQLEnum, Text
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class VacationType(str, enum.Enum):
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"
    DAY_OFF = "day_off"
    OTHER = "other"


class VacationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Vacation(Base):
    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vacation_type = Column(SQLEnum(VacationType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SQLEnum(VacationStatus), default=VacationStatus.PENDING, nullable=False)
    comment = Column(Text, nullable=True)
    approved_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
