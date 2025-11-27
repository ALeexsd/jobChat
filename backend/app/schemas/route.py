from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.route import RouteStatus, LocationStatus


class RouteLocationCreate(BaseModel):
    name: str
    address: Optional[str] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    order: int


class RouteLocationResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    description: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    order: int
    status: LocationStatus

    class Config:
        from_attributes = True


class RouteCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    assignee_ids: List[int] = []
    locations: List[RouteLocationCreate] = []


class RouteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RouteStatus] = None
    date: Optional[datetime] = None
    assignee_ids: Optional[List[int]] = None
    locations: Optional[List[RouteLocationCreate]] = None


class UserBasicInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True


class RouteAssigneeResponse(BaseModel):
    id: int
    user_id: int
    assigned_at: datetime
    user: Optional[UserBasicInfo] = None

    class Config:
        from_attributes = True


class RouteResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: RouteStatus
    date: datetime
    created_by_id: int
    created_at: datetime
    locations: List[RouteLocationResponse] = []
    assignees: List[RouteAssigneeResponse] = []

    class Config:
        from_attributes = True
