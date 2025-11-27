from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.vacation import VacationType, VacationStatus


class VacationCreate(BaseModel):
    vacation_type: VacationType
    start_date: date
    end_date: date
    comment: Optional[str] = None


class VacationUpdate(BaseModel):
    status: VacationStatus


class VacationResponse(BaseModel):
    id: int
    user_id: int
    vacation_type: VacationType
    start_date: date
    end_date: date
    status: VacationStatus
    comment: Optional[str]
    approved_by_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
