# Примеры использования

## Примеры API запросов

### Регистрация и вход

#### Регистрация нового пользователя
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-05-15"
  }'
```

#### Вход в систему
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

Ответ:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Работа с чатами

#### Создание группового чата
```bash
curl -X POST "http://localhost:8000/api/chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Команда разработки",
    "chat_type": "group",
    "member_ids": [2, 3, 4, 5]
  }'
```

#### Получение списка чатов
```bash
curl -X GET "http://localhost:8000/api/chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Отправка сообщения
```bash
curl -X POST "http://localhost:8000/api/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": 1,
    "content": "Привет, команда!",
    "message_type": "text"
  }'
```

#### Загрузка файла
```bash
curl -X POST "http://localhost:8000/api/messages/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/document.pdf"
```

### Работа с задачами

#### Создание задачи
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Реализовать новую функцию",
    "description": "Добавить возможность экспорта данных",
    "priority": "high",
    "deadline": "2024-12-31T23:59:59Z",
    "assignee_ids": [2, 3],
    "tags": "backend,api,export"
  }'
```

#### Обновление статуса задачи
```bash
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

#### Добавление комментария к задаче
```bash
curl -X POST "http://localhost:8000/api/tasks/1/comments" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Начал работу над задачей"
  }'
```

#### Добавление подзадачи
```bash
curl -X POST "http://localhost:8000/api/tasks/1/subtasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Создать API endpoint",
    "assignee_id": 2
  }'
```

### Работа с маршрутами

#### Создание маршрута
```bash
curl -X POST "http://localhost:8000/api/routes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Доставка утренняя",
    "description": "Маршрут доставки на утро",
    "date": "2024-01-15T08:00:00Z",
    "assignee_ids": [2],
    "locations": [
      {
        "name": "Склад",
        "address": "ул. Складская, 1",
        "description": "Загрузка товара",
        "order": 1
      },
      {
        "name": "Магазин №1",
        "address": "ул. Центральная, 10",
        "description": "Доставка партии А",
        "order": 2
      },
      {
        "name": "Магазин №2",
        "address": "ул. Ленина, 25",
        "description": "Доставка партии Б",
        "order": 3
      }
    ]
  }'
```

### Работа с заметками

#### Создание заметки
```bash
curl -X POST "http://localhost:8000/api/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Важная встреча",
    "content": "Обсудить новый проект с клиентом",
    "category": "work",
    "is_pinned": true,
    "tags": "meeting,important"
  }'
```

#### Создание заметки о пользователе
```bash
curl -X POST "http://localhost:8000/api/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Заметка об Иване",
    "content": "Отвечает за склад, связываться по вопросам поставок",
    "about_user_id": 5,
    "tags": "contacts"
  }'
```

### Работа с отпусками

#### Создание запроса на отпуск
```bash
curl -X POST "http://localhost:8000/api/vacations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vacation_type": "vacation",
    "start_date": "2024-07-01",
    "end_date": "2024-07-14",
    "comment": "Летний отпуск"
  }'
```

#### Утверждение отпуска (Admin/Manager)
```bash
curl -X PUT "http://localhost:8000/api/vacations/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved"
  }'
```

### Работа с уведомлениями

#### Получение непрочитанных уведомлений
```bash
curl -X GET "http://localhost:8000/api/notifications?unread_only=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Отметить уведомление как прочитанное
```bash
curl -X PATCH "http://localhost:8000/api/notifications/1/read" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Отметить все уведомления как прочитанные
```bash
curl -X PATCH "http://localhost:8000/api/notifications/read-all" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Примеры использования WebSocket

### JavaScript/TypeScript

```javascript
// Подключение к WebSocket
const token = 'YOUR_ACCESS_TOKEN';
const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

// Обработка подключения
ws.onopen = () => {
  console.log('WebSocket connected');
};

// Обработка входящих сообщений
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch (data.type) {
    case 'message':
      console.log('New message:', data);
      // Обновить UI с новым сообщением
      break;
      
    case 'typing':
      console.log('User typing:', data.user_id);
      // Показать индикатор печати
      break;
      
    case 'status_update':
      console.log('Status update:', data);
      // Обновить статус пользователя
      break;
  }
};

// Отправка сообщения
function sendMessage(chatId, content, userIds) {
  ws.send(JSON.stringify({
    type: 'message',
    chat_id: chatId,
    content: content,
    user_ids: userIds
  }));
}

// Отправка индикатора печати
function sendTypingIndicator(chatId, userIds) {
  ws.send(JSON.stringify({
    type: 'typing',
    chat_id: chatId,
    user_ids: userIds
  }));
}

// Обновление статуса
function updateStatus(status, userIds) {
  ws.send(JSON.stringify({
    type: 'status',
    status: status,
    user_ids: userIds
  }));
}

// Обработка ошибок
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Обработка закрытия соединения
ws.onclose = () => {
  console.log('WebSocket disconnected');
  // Попытка переподключения
  setTimeout(() => {
    // Переподключение
  }, 3000);
};
```

### Python

```python
import asyncio
import websockets
import json

async def connect_websocket():
    token = "YOUR_ACCESS_TOKEN"
    uri = f"ws://localhost:8000/ws?token={token}"
    
    async with websockets.connect(uri) as websocket:
        print("WebSocket connected")
        
        # Отправка сообщения
        await websocket.send(json.dumps({
            "type": "message",
            "chat_id": 1,
            "content": "Hello from Python!",
            "user_ids": [2, 3]
        }))
        
        # Получение сообщений
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received: {data}")
                
                if data['type'] == 'message':
                    print(f"New message: {data['content']}")
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

# Запуск
asyncio.run(connect_websocket())
```

## Примеры использования Frontend (Vue.js)

### Компонент чата

```vue
<template>
  <div class="chat">
    <div class="messages">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="['message', { 'own': message.sender_id === currentUserId }]"
      >
        <p>{{ message.content }}</p>
        <span class="time">{{ formatTime(message.created_at) }}</span>
      </div>
    </div>
    
    <div class="input-area">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        @input="handleTyping"
        placeholder="Введите сообщение..."
      />
      <button @click="sendMessage">Отправить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import websocket from '@/services/websocket'

const chatStore = useChatStore()
const messages = ref([])
const newMessage = ref('')
const currentUserId = ref(1)

onMounted(async () => {
  await chatStore.fetchMessages(1)
  messages.value = chatStore.messages
})

function sendMessage() {
  if (!newMessage.value.trim()) return
  
  chatStore.sendMessage(1, newMessage.value)
  newMessage.value = ''
}

function handleTyping() {
  websocket.sendTypingIndicator(1, [2, 3, 4])
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
```

### Компонент списка задач

```vue
<template>
  <div class="tasks">
    <div class="task-filters">
      <button
        v-for="status in statuses"
        :key="status"
        @click="filterByStatus(status)"
        :class="{ active: currentFilter === status }"
      >
        {{ status }}
      </button>
    </div>
    
    <div class="task-list">
      <div
        v-for="task in filteredTasks"
        :key="task.id"
        class="task-card"
        @click="openTask(task.id)"
      >
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <div class="task-meta">
          <span :class="['priority', task.priority]">
            {{ task.priority }}
          </span>
          <span class="deadline">
            {{ formatDate(task.deadline) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/task'

const taskStore = useTaskStore()
const tasks = ref([])
const currentFilter = ref('all')
const statuses = ['all', 'todo', 'in_progress', 'done']

onMounted(async () => {
  await taskStore.fetchTasks()
  tasks.value = taskStore.tasks
})

const filteredTasks = computed(() => {
  if (currentFilter.value === 'all') {
    return tasks.value
  }
  return tasks.value.filter(task => task.status === currentFilter.value)
})

function filterByStatus(status) {
  currentFilter.value = status
}

function openTask(taskId) {
  // Открыть детали задачи
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('ru-RU')
}
</script>
```

## Примеры Docker команд

### Управление контейнерами

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск конкретного сервиса
docker-compose restart backend

# Просмотр логов
docker-compose logs -f backend

# Просмотр статуса
docker-compose ps

# Выполнение команды в контейнере
docker-compose exec backend python scripts/create_admin.py

# Подключение к БД
docker-compose exec postgres psql -U chatuser -d chatdb
```

### Работа с миграциями

```bash
# Создание новой миграции
docker-compose exec backend alembic revision --autogenerate -m "add new field"

# Применение миграций
docker-compose exec backend alembic upgrade head

# Откат последней миграции
docker-compose exec backend alembic downgrade -1

# Просмотр истории миграций
docker-compose exec backend alembic history

# Просмотр текущей версии
docker-compose exec backend alembic current
```

### Бэкап и восстановление БД

```bash
# Создание бэкапа
docker-compose exec postgres pg_dump -U chatuser chatdb > backup.sql

# Восстановление из бэкапа
docker-compose exec -T postgres psql -U chatuser chatdb < backup.sql

# Бэкап с сжатием
docker-compose exec postgres pg_dump -U chatuser chatdb | gzip > backup.sql.gz

# Восстановление из сжатого бэкапа
gunzip < backup.sql.gz | docker-compose exec -T postgres psql -U chatuser chatdb
```

## Примеры тестов

### Backend тесты (PyTest)

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "birth_date": "1990-01-01"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

@pytest.mark.asyncio
async def test_create_chat():
    # Предполагается, что пользователь уже залогинен
    token = "test_token"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chats",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Test Chat",
                "chat_type": "group",
                "member_ids": [2, 3]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Chat"
```

Эти примеры помогут вам быстро начать работу с API и понять, как использовать различные функции системы.
