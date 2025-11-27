from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter()


@router.post("/", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_note = Note(
        user_id=current_user.id,
        title=note_data.title,
        content=note_data.content,
        category=note_data.category,
        is_pinned=note_data.is_pinned,
        about_user_id=note_data.about_user_id,
        tags=note_data.tags
    )
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    
    return new_note


@router.get("/", response_model=List[NoteResponse])
async def get_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Note)
        .where(Note.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    notes = result.scalars().all()
    return notes


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for field, value in note_update.dict(exclude_unset=True).items():
        setattr(note, field, value)
    
    await db.commit()
    await db.refresh(note)
    
    return note


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    
    return {"message": "Note deleted"}
