# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

Все защищенные endpoints требуют JWT токен в заголовке:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### POST /auth/register
Регистрация нового пользователя

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1990-01-15"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1990-01-15",
  "role": "employee",
  "status": "offline",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### POST /auth/login
Вход в систему

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### POST /auth/refresh
Обновление access токена

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Users

#### GET /users/me
Получить информацию о текущем пользователе

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1990-01-15",
  "avatar_url": null,
  "role": "employee",
  "status": "online",
  "last_seen": "2024-01-01T10:00:00Z",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### PUT /users/me
Обновить профиль текущего пользователя

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "avatar_url": "/media/avatar.jpg",
  "status": "online"
}
```

#### GET /users
Получить список пользователей

**Query Parameters:**
- `skip` (int): Пропустить N записей (default: 0)
- `limit` (int): Лимит записей (default: 100)
- `search` (string): Поиск по имени/username

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "status": "online",
    ...
  }
]
```

#### GET /users/birthdays
Получить список ближайших дней рождения

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-01-15",
    ...
  }
]
```

### Chats

#### POST /chats
Создать новый чат

**Request:**
```json
{
  "name": "Project Team",
  "chat_type": "group",
  "member_ids": [2, 3, 4]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Project Team",
  "chat_type": "group",
  "avatar_url": null,
  "created_at": "2024-01-01T10:00:00Z",
  "members": [
    {
      "id": 1,
      "user_id": 1,
      "role": "owner",
      "joined_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### GET /chats
Получить список чатов пользователя

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Project Team",
    "chat_type": "group",
    "avatar_url": null,
    "created_at": "2024-01-01T10:00:00Z",
    "members": [...]
  }
]
```

#### GET /chats/{chat_id}
Получить информацию о чате

#### PUT /chats/{chat_id}
Обновить чат

#### DELETE /chats/{chat_id}
Удалить чат

### Messages

#### POST /messages
Отправить сообщение

**Request:**
```json
{
  "chat_id": 1,
  "content": "Hello, team!",
  "message_type": "text",
  "reply_to_id": null
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "chat_id": 1,
  "sender_id": 1,
  "content": "Hello, team!",
  "message_type": "text",
  "status": "sent",
  "is_edited": false,
  "is_deleted": false,
  "created_at": "2024-01-01T10:00:00Z",
  "attachments": []
}
```

#### GET /messages/chat/{chat_id}
Получить сообщения чата

**Query Parameters:**
- `skip` (int): Пропустить N сообщений
- `limit` (int): Лимит сообщений (default: 50)

#### PUT /messages/{message_id}
Редактировать сообщение

#### DELETE /messages/{message_id}
Удалить сообщение

#### POST /messages/{message_id}/reactions
Добавить/удалить реакцию

**Request:**
```json
{
  "emoji": "👍"
}
```

#### POST /messages/upload
Загрузить файл

**Request:** `multipart/form-data`
- `file`: File

**Response:** `200 OK`
```json
{
  "file_name": "document.pdf",
  "file_path": "/media/uuid.pdf",
  "file_type": "application/pdf",
  "file_size": 1024000
}
```

#### GET /messages/search
Поиск сообщений

**Query Parameters:**
- `query` (string): Поисковый запрос
- `chat_id` (int, optional): ID чата

### Tasks

#### POST /tasks
Создать задачу

**Request:**
```json
{
  "title": "Implement feature X",
  "description": "Detailed description",
  "priority": "high",
  "deadline": "2024-12-31T23:59:59Z",
  "assignee_ids": [2, 3],
  "tags": "backend,api"
}
```

#### GET /tasks
Получить список задач

#### GET /tasks/{task_id}
Получить задачу

#### PUT /tasks/{task_id}
Обновить задачу

#### POST /tasks/{task_id}/comments
Добавить комментарий

**Request:**
```json
{
  "content": "Great progress!"
}
```

#### POST /tasks/{task_id}/subtasks
Добавить подзадачу

**Request:**
```json
{
  "title": "Subtask 1",
  "assignee_id": 2
}
```

### Routes

#### POST /routes
Создать маршрут

**Request:**
```json
{
  "title": "Delivery Route 1",
  "description": "Morning deliveries",
  "date": "2024-01-15T08:00:00Z",
  "assignee_ids": [2],
  "locations": [
    {
      "name": "Location 1",
      "address": "123 Main St",
      "description": "First stop",
      "order": 1
    }
  ]
}
```

#### GET /routes
Получить список маршрутов

#### GET /routes/{route_id}
Получить маршрут

#### PUT /routes/{route_id}
Обновить маршрут

### Notes

#### POST /notes
Создать заметку

**Request:**
```json
{
  "title": "Important note",
  "content": "Note content",
  "category": "work",
  "is_pinned": false,
  "about_user_id": null,
  "tags": "important,work"
}
```

#### GET /notes
Получить заметки

#### PUT /notes/{note_id}
Обновить заметку

#### DELETE /notes/{note_id}
Удалить заметку

### Vacations

#### POST /vacations
Создать запрос на отпуск

**Request:**
```json
{
  "vacation_type": "vacation",
  "start_date": "2024-07-01",
  "end_date": "2024-07-14",
  "comment": "Summer vacation"
}
```

#### GET /vacations
Получить список отпусков

#### PUT /vacations/{vacation_id}
Утвердить/отклонить отпуск (только Admin/Manager)

**Request:**
```json
{
  "status": "approved"
}
```

### Notifications

#### GET /notifications
Получить уведомления

**Query Parameters:**
- `skip` (int): Пропустить N записей
- `limit` (int): Лимит записей (default: 50)
- `unread_only` (bool): Только непрочитанные

#### PATCH /notifications/{notification_id}/read
Отметить как прочитанное

#### PATCH /notifications/read-all
Отметить все как прочитанные

## WebSocket

### Connection
```
ws://localhost:8000/ws?token=<access_token>
```

### Message Types

#### Send Message
```json
{
  "type": "message",
  "chat_id": 1,
  "content": "Hello!",
  "user_ids": [2, 3, 4]
}
```

#### Typing Indicator
```json
{
  "type": "typing",
  "chat_id": 1,
  "user_ids": [2, 3, 4]
}
```

#### Status Update
```json
{
  "type": "status",
  "status": "online",
  "user_ids": [2, 3, 4]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

- 100 requests per minute per user
- 1000 requests per hour per user

## Pagination

Все list endpoints поддерживают пагинацию:
- `skip`: количество пропущенных записей
- `limit`: максимальное количество записей

## Interactive Documentation

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
