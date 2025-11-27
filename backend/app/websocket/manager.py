from fastapi import WebSocket, WebSocketDisconnect, Query
from typing import Dict, List, Set, Optional
import json
from datetime import datetime
from jose import jwt, JWTError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # user_id -> List[WebSocket]
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # chat_id -> Set[user_id]
        self.chat_members: Dict[int, Set[int]] = {}
        # user_id -> Set[chat_id]
        self.user_chats: Dict[int, Set[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Подключение пользователя"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Отключение пользователя"""
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                logger.info(f"User {user_id} disconnected")
            except ValueError:
                pass
    
    def is_user_online(self, user_id: int) -> bool:
        """Проверка, онлайн ли пользователь"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
    
    def get_online_users(self) -> List[int]:
        """Получить список онлайн пользователей"""
        return list(self.active_connections.keys())
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Отправка личного сообщения пользователю"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    disconnected.append(connection)
            
            # Удаляем отключенные соединения
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def broadcast_to_chat(self, message: dict, chat_id: int, exclude_user_id: int = None):
        """Отправка сообщения всем участникам чата"""
        if chat_id in self.chat_members:
            for user_id in self.chat_members[chat_id]:
                if exclude_user_id and user_id == exclude_user_id:
                    continue
                await self.send_personal_message(message, user_id)
    
    async def broadcast_to_users(self, message: dict, user_ids: List[int]):
        """Отправка сообщения списку пользователей"""
        for user_id in user_ids:
            await self.send_personal_message(message, user_id)
    
    def add_user_to_chat(self, user_id: int, chat_id: int):
        """Добавить пользователя в чат"""
        if chat_id not in self.chat_members:
            self.chat_members[chat_id] = set()
        self.chat_members[chat_id].add(user_id)
        
        if user_id not in self.user_chats:
            self.user_chats[user_id] = set()
        self.user_chats[user_id].add(chat_id)
    
    def remove_user_from_chat(self, user_id: int, chat_id: int):
        """Удалить пользователя из чата"""
        if chat_id in self.chat_members:
            self.chat_members[chat_id].discard(user_id)
        if user_id in self.user_chats:
            self.user_chats[user_id].discard(chat_id)
    
    async def send_typing_indicator(self, chat_id: int, user_id: int, is_typing: bool):
        """Отправка индикатора печати"""
        message = {
            "type": "typing",
            "chat_id": chat_id,
            "user_id": user_id,
            "is_typing": is_typing,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_chat(message, chat_id, exclude_user_id=user_id)
    
    async def send_message_notification(self, chat_id: int, message_data: dict, sender_id: int):
        """Отправка уведомления о новом сообщении"""
        notification = {
            "type": "new_message",
            "chat_id": chat_id,
            "message": message_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.info(f"Sending new_message notification for chat {chat_id} to all members except {sender_id}")
        
        # Отправляем всем участникам чата
        if chat_id in self.chat_members:
            logger.info(f"Chat {chat_id} has {len(self.chat_members[chat_id])} members")
            for user_id in self.chat_members[chat_id]:
                if user_id != sender_id:
                    await self.send_personal_message(notification, user_id)
                    logger.info(f"Sent notification to user {user_id}")
        else:
            logger.warning(f"Chat {chat_id} has no members in WebSocket manager")
            # Отправляем всем подключенным пользователям (fallback)
            for user_id in self.active_connections.keys():
                if user_id != sender_id:
                    await self.send_personal_message(notification, user_id)
    
    async def send_message_update(self, chat_id: int, message_id: int, content: str):
        """Отправка уведомления об обновлении сообщения"""
        notification = {
            "type": "message_updated",
            "chat_id": chat_id,
            "message_id": message_id,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_chat(notification, chat_id)
    
    async def send_message_delete(self, chat_id: int, message_id: int):
        """Отправка уведомления об удалении сообщения"""
        notification = {
            "type": "message_deleted",
            "chat_id": chat_id,
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_chat(notification, chat_id)
    
    async def send_user_status(self, user_id: int, status: str):
        """Отправка обновления статуса пользователя"""
        message = {
            "type": "user_status",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        # Отправить всем чатам, где есть этот пользователь
        if user_id in self.user_chats:
            for chat_id in self.user_chats[user_id]:
                await self.broadcast_to_chat(message, chat_id, exclude_user_id=user_id)
    
    async def send_task_notification(self, user_id: int, task_id: int, task_title: str, assigned_by: int):
        """Отправка уведомления о назначении задачи"""
        message = {
            "type": "task_assigned",
            "task_id": task_id,
            "task_title": task_title,
            "assigned_by": assigned_by,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.info(f"📋 Preparing to send task notification to user {user_id}")
        logger.info(f"📋 User {user_id} online: {self.is_user_online(user_id)}")
        logger.info(f"📋 Message: {message}")
        await self.send_personal_message(message, user_id)
        logger.info(f"✅ Sent task notification to user {user_id} for task {task_id}")
    
    async def send_route_notification(self, user_id: int, route_id: int, route_title: str, assigned_by: int):
        """Отправка уведомления о назначении маршрута"""
        message = {
            "type": "route_assigned",
            "route_id": route_id,
            "route_title": route_title,
            "assigned_by": assigned_by,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.info(f"🗺️ Preparing to send route notification to user {user_id}")
        logger.info(f"🗺️ User {user_id} online: {self.is_user_online(user_id)}")
        await self.send_personal_message(message, user_id)
        logger.info(f"✅ Sent route notification to user {user_id} for route {route_id}")


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    """WebSocket endpoint для реального времени"""
    logger.info(f"WebSocket connection attempt with token: {token[:20] if token else 'None'}...")
    
    # Валидация JWT токена
    if not token:
        logger.error("No token provided")
        await websocket.close(code=1008, reason="No token provided")
        return
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if user_id is None:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Подключаем пользователя
    await manager.connect(websocket, user_id)
    
    # Загружаем все чаты пользователя и добавляем его в них
    from app.core.database import async_session_maker
    from app.models.chat import ChatMember
    from app.models.user import User, UserStatus
    from sqlalchemy import select
    
    async with async_session_maker() as db:
        # Получаем чаты пользователя
        result = await db.execute(
            select(ChatMember.chat_id).where(ChatMember.user_id == user_id)
        )
        chat_ids = [row[0] for row in result.all()]
        
        for chat_id in chat_ids:
            manager.add_user_to_chat(user_id, chat_id)
            logger.info(f"Added user {user_id} to chat {chat_id}")
        
        # Устанавливаем статус онлайн
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.status = UserStatus.ONLINE
            user.last_seen = datetime.utcnow()
            await db.commit()
            logger.info(f"User {user_id} status set to online")
    
    # Отправляем подтверждение подключения
    await websocket.send_json({
        "type": "connected",
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Уведомляем других пользователей о статусе онлайн
    await manager.send_user_status(user_id, "online")
    
    try:
        while True:
            # Получаем данные от клиента
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            
            # Обработка разных типов сообщений
            if message_type == "ping":
                # Ответ на ping
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif message_type == "typing":
                # Индикатор печати
                chat_id = message_data.get("chat_id")
                is_typing = message_data.get("is_typing", True)
                await manager.send_typing_indicator(chat_id, user_id, is_typing)
            
            elif message_type == "join_chat":
                # Присоединение к чату
                chat_id = message_data.get("chat_id")
                manager.add_user_to_chat(user_id, chat_id)
                logger.info(f"User {user_id} joined chat {chat_id}")
            
            elif message_type == "leave_chat":
                # Выход из чата
                chat_id = message_data.get("chat_id")
                manager.remove_user_from_chat(user_id, chat_id)
                logger.info(f"User {user_id} left chat {chat_id}")
            
            elif message_type == "status":
                # Обновление статуса
                status = message_data.get("status")
                await manager.send_user_status(user_id, status)
            
            elif message_type == "read_messages":
                # Отметка сообщений как прочитанных
                chat_id = message_data.get("chat_id")
                read_notification = {
                    "type": "messages_read",
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
                # Отправляем всем участникам чата, включая отправителя
                await manager.broadcast_to_chat(read_notification, chat_id)
                logger.info(f"User {user_id} marked messages as read in chat {chat_id}")
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"User {user_id} disconnected")
        
        # Устанавливаем статус офлайн в БД
        from app.core.database import async_session_maker
        from app.models.user import User, UserStatus
        from sqlalchemy import select
        
        async with async_session_maker() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user.status = UserStatus.OFFLINE
                user.last_seen = datetime.utcnow()
                await db.commit()
                logger.info(f"User {user_id} status set to offline")
        
        # Уведомляем других пользователей о статусе офлайн
        await manager.send_user_status(user_id, "offline")
        
        # Уведомление об отключении
        if user_id in manager.user_chats:
            for chat_id in manager.user_chats[user_id]:
                await manager.broadcast_to_chat({
                    "type": "user_offline",
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }, chat_id)
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)
        
        # Устанавливаем статус офлайн при ошибке
        from app.core.database import async_session_maker
        from app.models.user import User, UserStatus
        from sqlalchemy import select
        
        async with async_session_maker() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user.status = UserStatus.OFFLINE
                user.last_seen = datetime.utcnow()
                await db.commit()
