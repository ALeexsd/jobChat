from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class RouteStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LocationStatus(str, enum.Enum):
    PENDING = "pending"
    ARRIVED = "arrived"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(RouteStatus), default=RouteStatus.PENDING, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    locations = relationship("RouteLocation", back_populates="route", cascade="all, delete-orphan")
    assignees = relationship("RouteAssignee", back_populates="route", cascade="all, delete-orphan")


class RouteLocation(Base):
    __tablename__ = "route_locations"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    contact_name = Column(String, nullable=True)  # ФИО контактного лица
    contact_phone = Column(String, nullable=True)  # Телефон контактного лица
    order = Column(Integer, nullable=False)
    status = Column(SQLEnum(LocationStatus), default=LocationStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    route = relationship("Route", back_populates="locations")


class RouteAssignee(Base):
    __tablename__ = "route_assignees"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    route = relationship("Route", back_populates="assignees")
    user = relationship("User")
