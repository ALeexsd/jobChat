from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.vacation import Vacation
from app.schemas.vacation import VacationCreate, VacationResponse, VacationUpdate

router = APIRouter()


@router.post("/", response_model=VacationResponse)
async def create_vacation(
    vacation_data: VacationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_vacation = Vacation(
        user_id=current_user.id,
        vacation_type=vacation_data.vacation_type,
        start_date=vacation_data.start_date,
        end_date=vacation_data.end_date,
        comment=vacation_data.comment
    )
    db.add(new_vacation)
    await db.commit()
    await db.refresh(new_vacation)
    
    return new_vacation


@router.get("/")
async def get_vacations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Vacation).offset(skip).limit(limit)
    )
    vacations = result.scalars().all()
    
    # Получаем информацию о пользователях
    user_ids = [v.user_id for v in vacations]
    users_result = await db.execute(
        select(User).where(User.id.in_(user_ids))
    )
    users = {u.id: u for u in users_result.scalars().all()}
    
    # Формируем ответ с информацией о пользователях
    response = []
    for vacation in vacations:
        user = users.get(vacation.user_id)
        vacation_dict = {
            "id": vacation.id,
            "user_id": vacation.user_id,
            "user_name": f"{user.first_name} {user.last_name}" if user else "Неизвестный пользователь",
            "vacation_type": vacation.vacation_type,
            "start_date": vacation.start_date,
            "end_date": vacation.end_date,
            "status": vacation.status,
            "reason": vacation.comment,
            "approved_by_id": vacation.approved_by_id,
            "created_at": vacation.created_at
        }
        response.append(vacation_dict)
    
    return response


@router.put("/{vacation_id}", response_model=VacationResponse)
async def update_vacation_status(
    vacation_id: int,
    vacation_update: VacationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    result = await db.execute(select(Vacation).where(Vacation.id == vacation_id))
    vacation = result.scalar_one_or_none()
    
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    
    vacation.status = vacation_update.status
    vacation.approved_by_id = current_user.id
    
    await db.commit()
    await db.refresh(vacation)
    
    return vacation
