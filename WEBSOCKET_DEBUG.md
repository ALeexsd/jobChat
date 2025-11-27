# 🐛 Отладка WebSocket

## Проблема
WebSocket не подключается, сообщения не доставляются в реальном времени.

## Проверка

### 1. Откройте консоль браузера (F12)

Перейдите на http://localhost:3000 и войдите в систему.

В консоли должны быть логи:
```
🔌 Connecting to WebSocket from ChatsView...
✅ WebSocket connected in ChatsView
📡 Subscribing to WebSocket events in ChatsView
```

Если этих логов нет - WebSocket не подключается.

### 2. Проверьте WebSocket URL

В консоли браузера выполните:
```javascript
console.log(import.meta.env.VITE_WS_URL)
```

Должно быть: `ws://localhost:8000`

### 3. Проверьте подключение вручную

В консоли браузера:
```javascript
// Получите токен
const token = localStorage.getItem('access_token')
console.log('Token:', token)

// Попробуйте подключиться
const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`)

ws.onopen = () => console.log('✅ WebSocket opened')
ws.onerror = (e) => console.error('❌ WebSocket error:', e)
ws.onmessage = (e) => console.log('📨 Message:', e.data)
ws.onclose = (e) => console.log('🔌 WebSocket closed:', e.code, e.reason)
```

### 4. Проверьте backend логи

```bash
docker logs chat_backend -f
```

При подключении должны появиться логи:
```
INFO:     User X connected. Total connections: Y
INFO:     Added user X to chat Y
```

## Возможные причины

### 1. Токен не передается
Проверьте, что токен есть в localStorage:
```javascript
localStorage.getItem('access_token')
```

### 2. CORS блокирует WebSocket
Проверьте в консоли, нет ли ошибок CORS.

### 3. Backend не запущен
```bash
docker ps | grep chat_backend
```

### 4. Неправильный URL
Проверьте файл `frontend/.env`:
```bash
cat frontend/.env
```

Должно быть:
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

## Решение

### Вариант 1: Перезапуск
```bash
docker-compose down
docker-compose up -d
```

### Вариант 2: Очистка кэша
1. Откройте DevTools (F12)
2. Правый клик на кнопке обновления
3. Выберите "Очистить кэш и жесткая перезагрузка"

### Вариант 3: Проверка кода

Откройте `frontend/src/services/websocket.js` и добавьте больше логов:

```javascript
connect() {
  console.log('🔌 WebSocket connect() called')
  console.log('Current state:', this.ws?.readyState)
  console.log('Is connecting:', this.isConnecting)
  
  // ... остальной код
  
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  const url = `${wsUrl}/ws?token=${token}`
  
  console.log('🔗 Connecting to:', url)
  this.ws = new WebSocket(url)
  
  this.ws.onopen = () => {
    console.log('✅ WebSocket onopen fired')
    // ... остальной код
  }
  
  this.ws.onerror = (error) => {
    console.error('❌ WebSocket onerror fired:', error)
    // ... остальной код
  }
}
```

## Тест отправки сообщения

1. Откройте два окна браузера
2. Войдите как user1 в первом, user2 во втором
3. Откройте консоль (F12) в обоих окнах
4. Отправьте сообщение из первого окна
5. Проверьте логи во втором окне:

**Должно быть:**
```
📨 New message in chat list: {chat_id: X, message: {...}}
📊 Unread count for chat X: 1
⬆️ Moved chat X to top
```

**Если нет:**
- Проверьте, что WebSocket подключен: `websocket.isConnected()` должно быть `true`
- Проверьте backend логи на наличие `Sending new_message notification`

## Backend логи для отладки

Добавьте в `backend/app/websocket/manager.py`:

```python
async def send_message_notification(self, chat_id: int, message_data: dict, sender_id: int):
    logger.info(f"=== SEND MESSAGE NOTIFICATION ===")
    logger.info(f"Chat ID: {chat_id}")
    logger.info(f"Sender ID: {sender_id}")
    logger.info(f"Message: {message_data}")
    logger.info(f"Active connections: {list(self.active_connections.keys())}")
    logger.info(f"Chat members: {self.chat_members.get(chat_id, set())}")
    
    # ... остальной код
```

Затем перезапустите backend:
```bash
docker restart chat_backend
```

И проверьте логи:
```bash
docker logs chat_backend -f
```

---

**Следующий шаг:** Откройте http://localhost:3000, войдите и проверьте консоль браузера.
