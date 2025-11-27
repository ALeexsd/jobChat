from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, extract, func
from typing import List
from datetime import datetime, date

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserStatus
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(User).where(User.is_active == True)
    
    if search:
        query = query.where(
            or_(
                User.username.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%")
            )
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users


@router.get("/birthdays", response_model=List[UserResponse])
async def get_upcoming_birthdays(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    current_month = today.month
    current_day = today.day
    
    # Получаем пользователей с днями рождения в текущем месяце
    query = select(User).where(
        User.is_active == True,
        User.birth_date.isnot(None),
        extract('month', User.birth_date) == current_month,
        extract('day', User.birth_date) >= current_day
    ).order_by(extract('day', User.birth_date))
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка прав администратора
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Получаем пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Обновляем поля
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.patch("/status", response_model=UserResponse)
async def update_status(
    status: UserStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.status = status
    current_user.last_seen = datetime.utcnow()
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


from fastapi import UploadFile, File
import os
import uuid
from app.core.config import settings


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверка типа файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Проверка размера файла
    content = await file.read()
    file_size = len(content)
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    
    # Сохранение файла
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"avatar_{current_user.id}_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join("media", "avatars", file_name)
    
    # Создание директории если не существует
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Удаление старого аватара если есть
    if current_user.avatar:
        old_path = current_user.avatar.replace('/media/', 'media/')
        if os.path.exists(old_path):
            os.remove(old_path)
    
    # Сохранение нового файла
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Обновление пользователя
    current_user.avatar = f"/media/avatars/{file_name}"
    await db.commit()
    await db.refresh(current_user)
    
    return current_user
