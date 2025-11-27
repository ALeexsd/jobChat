from fastapi import FastAPI, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import auth, users, chats, messages, tasks, routes, notes, vacations, notifications
from app.websocket.manager import websocket_endpoint

app = FastAPI(title="Corporate Messenger API", version="1.0.0")

# CORS - разрешаем все источники для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

# Статические файлы
os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(vacations.router, prefix="/api/vacations", tags=["Vacations"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

# WebSocket
@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket endpoint"""
    # Получаем токен из query параметров
    token = websocket.query_params.get('token')
    await websocket_endpoint(websocket, token)


@app.get("/")
async def root():
    return {"message": "Corporate Messenger API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
