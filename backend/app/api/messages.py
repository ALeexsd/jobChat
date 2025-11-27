from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import List
import os
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.chat import Chat, ChatMember
from app.models.message import Message, MessageReaction, MessageAttachment, MessageType
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate, MessageReactionCreate
from app.websocket.manager import manager

router = APIRouter()


@router.post("/", response_model=MessageResponse)
async def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверка доступа к чату
    result = await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == message_data.chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Access denied")
    
    new_message = Message(
        chat_id=message_data.chat_id,
        sender_id=current_user.id,
        content=message_data.content,
        message_type=message_data.message_type,
        reply_to_id=message_data.reply_to_id
    )
    
    db.add(new_message)
    await db.flush()
    
    # Добавляем вложение если есть
    if message_data.attachment:
        attachment = MessageAttachment(
            message_id=new_message.id,
            file_name=message_data.attachment.file_name,
            file_path=message_data.attachment.file_path,
            file_type=message_data.attachment.file_type,
            file_size=message_data.attachment.file_size
        )
        db.add(attachment)
    
    await db.commit()
    await db.refresh(new_message, ['attachments'])
    
    # Отправляем уведомление через WebSocket
    await manager.send_message_notification(
        message_data.chat_id,
        {
            "id": new_message.id,
            "content": new_message.content,
            "sender_id": current_user.id,
            "created_at": new_message.created_at.isoformat(),
            "message_type": new_message.message_type
        },
        current_user.id
    )
    
    return new_message


@router.get("/chat/{chat_id}", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверка доступа
    result = await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Access denied")
    
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id, Message.is_deleted == False)
        .options(selectinload(Message.attachments))
        .order_by(Message.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    messages = result.scalars().all()
    
    return messages


@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only edit own messages")
    
    message.content = message_update.content
    message.is_edited = True
    
    await db.commit()
    await db.refresh(message)
    
    # Отправляем уведомление через WebSocket
    await manager.send_message_update(message.chat_id, message.id, message.content)
    
    return message


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only delete own messages")
    
    message.is_deleted = True
    message.content = None
    
    await db.commit()
    
    # Отправляем уведомление через WebSocket
    await manager.send_message_delete(message.chat_id, message.id)
    
    return {"message": "Message deleted"}


@router.post("/{message_id}/reactions")
async def add_reaction(
    message_id: int,
    reaction_data: MessageReactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверка существования сообщения
    result = await db.execute(select(Message).where(Message.id == message_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Проверка существующей реакции
    result = await db.execute(
        select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id,
            MessageReaction.emoji == reaction_data.emoji
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        await db.delete(existing)
    else:
        new_reaction = MessageReaction(
            message_id=message_id,
            user_id=current_user.id,
            emoji=reaction_data.emoji
        )
        db.add(new_reaction)
    
    await db.commit()
    
    return {"message": "Reaction updated"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        # Проверка размера файла
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Создаем директорию media если её нет
        os.makedirs("media", exist_ok=True)
        
        # Сохранение файла
        file_ext = os.path.splitext(file.filename)[1] if file.filename else ".bin"
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join("media", file_name)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "file_name": file.filename or "file",
            "file_path": f"/media/{file_name}",
            "file_type": file.content_type or "application/octet-stream",
            "file_size": file_size
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/search")
async def search_messages(
    query: str,
    chat_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Базовый запрос
    stmt = select(Message).where(
        Message.is_deleted == False,
        Message.content.ilike(f"%{query}%")
    )
    
    # Фильтр по чату
    if chat_id:
        stmt = stmt.where(Message.chat_id == chat_id)
    else:
        # Только чаты пользователя
        stmt = stmt.join(ChatMember).where(ChatMember.user_id == current_user.id)
    
    result = await db.execute(stmt.limit(50))
    messages = result.scalars().all()
    
    return messages


@router.post("/{message_id}/pin")
async def pin_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Закрепить сообщение"""
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Проверка доступа к чату
    result = await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == message.chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    message.is_pinned = True
    await db.commit()
    
    return {"status": "pinned", "message_id": message_id}


@router.delete("/{message_id}/pin")
async def unpin_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Открепить сообщение"""
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Проверка доступа к чату
    result = await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == message.chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    message.is_pinned = False
    await db.commit()
    
    return {"status": "unpinned", "message_id": message_id}


@router.get("/chat/{chat_id}/pinned", response_model=List[MessageResponse])
async def get_pinned_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить закрепленные сообщения чата"""
    # Проверка доступа к чату
    result = await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Получаем закрепленные сообщения
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id, Message.is_pinned == True, Message.is_deleted == False)
        .order_by(Message.created_at.desc())
    )
    messages = result.scalars().all()
    
    return messages
