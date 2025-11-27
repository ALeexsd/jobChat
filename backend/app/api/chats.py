from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import Chat, ChatMember, ChatType, ChatMemberRole
from app.models.message import Message
from app.schemas.chat import ChatCreate, ChatResponse, ChatUpdate

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Создание чата
    new_chat = Chat(
        name=chat_data.name,
        chat_type=chat_data.chat_type
    )
    db.add(new_chat)
    await db.flush()
    
    # Добавление создателя как владельца
    creator_member = ChatMember(
        chat_id=new_chat.id,
        user_id=current_user.id,
        role=ChatMemberRole.OWNER
    )
    db.add(creator_member)
    
    # Добавление остальных участников
    for member_id in chat_data.member_ids:
        if member_id != current_user.id:
            member = ChatMember(
                chat_id=new_chat.id,
                user_id=member_id,
                role=ChatMemberRole.MEMBER
            )
            db.add(member)
    
    await db.commit()
    await db.refresh(new_chat)
    
    # Загрузка с members
    result = await db.execute(
        select(Chat).options(selectinload(Chat.members)).where(Chat.id == new_chat.id)
    )
    chat = result.scalar_one()
    
    return chat


@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Получаем все чаты пользователя
    result = await db.execute(
        select(Chat)
        .join(ChatMember)
        .where(ChatMember.user_id == current_user.id)
        .options(selectinload(Chat.members))
    )
    chats = result.scalars().all()
    
    # Добавляем последнее сообщение для каждого чата
    chat_responses = []
    for chat in chats:
        # Получаем последнее сообщение
        last_msg_result = await db.execute(
            select(Message)
            .where(Message.chat_id == chat.id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        last_message = last_msg_result.scalar_one_or_none()
        
        # Формируем ответ
        chat_dict = {
            "id": chat.id,
            "name": chat.name,
            "chat_type": chat.chat_type,
            "avatar_url": chat.avatar_url,
            "created_at": chat.created_at,
            "members": chat.members,
            "last_message": {
                "content": last_message.content,
                "created_at": last_message.created_at
            } if last_message else None
        }
        chat_responses.append(chat_dict)
    
    # Сортируем по времени последнего сообщения (новые сверху)
    chat_responses.sort(key=lambda x: x["last_message"]["created_at"] if x["last_message"] else datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    
    return chat_responses


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.members))
        .where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Проверка доступа
    is_member = any(m.user_id == current_user.id for m in chat.members)
    if not is_member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.members))
        .where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Проверка прав (только владелец или админ)
    member = next((m for m in chat.members if m.user_id == current_user.id), None)
    if not member or member.role not in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    for field, value in chat_update.dict(exclude_unset=True).items():
        setattr(chat, field, value)
    
    await db.commit()
    await db.refresh(chat)
    
    return chat


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.members))
        .where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Только владелец может удалить чат
    member = next((m for m in chat.members if m.user_id == current_user.id), None)
    if not member or member.role != ChatMemberRole.OWNER:
        raise HTTPException(status_code=403, detail="Only owner can delete chat")
    
    await db.delete(chat)
    await db.commit()
    
    return {"message": "Chat deleted successfully"}


@router.get("/{chat_id}/messages")
async def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, что пользователь является участником чата
    member_result = await db.execute(
        select(ChatMember)
        .where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Получаем сообщения с вложениями
    result = await db.execute(
        select(Message)
        .options(selectinload(Message.attachments))
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    return messages


@router.delete("/{chat_id}/messages")
async def clear_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, что пользователь является участником чата
    member_result = await db.execute(
        select(ChatMember)
        .where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Удаляем все сообщения чата
    from sqlalchemy import delete
    await db.execute(
        delete(Message).where(Message.chat_id == chat_id)
    )
    await db.commit()
    
    return {"message": "Chat history cleared"}


@router.get("/{chat_id}/unread-count")
async def get_unread_count(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить количество непрочитанных сообщений в чате"""
    # Проверяем, что пользователь является участником чата
    member_result = await db.execute(
        select(ChatMember)
        .where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Временно возвращаем 0 до применения миграции
    # TODO: Реализовать подсчет после добавления поля last_read_at
    return {"count": 0}


@router.post("/{chat_id}/mark-read")
async def mark_messages_as_read(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отметить все сообщения в чате как прочитанные"""
    # Проверяем, что пользователь является участником чата
    member_result = await db.execute(
        select(ChatMember)
        .where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Временно отключено до применения миграции
    # member.last_read_at = datetime.utcnow()
    # await db.commit()
    
    return {"message": "Messages marked as read"}
