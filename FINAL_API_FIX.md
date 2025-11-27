# Финальное исправление API и Service Worker

## Проблемы
1. API запросы шли без слэша в конце (`/api/routes` вместо `/api/routes/`)
2. FastAPI делал редирект 307, что вызывало CORS ошибки
3. Service Worker перехватывал запросы и пытался их обработать

## Исправления

### 1. API Interceptor (frontend/src/services/api.js)
Добавлен автоматический слэш в конец URL:
```javascript
// Добавляем слэш в конец URL, если его нет
if (config.url && !config.url.endsWith('/') && !config.url.includes('?')) {
  config.url = config.url + '/'
}
```

**Теперь:**
- `/routes` → `/routes/`
- `/tasks` → `/tasks/`
- `/notes` → `/notes/`
- `/vacations` → `/vacations/`

### 2. Service Worker (frontend/public/sw.js)
Полностью игнорирует API запросы:
```javascript
// Полностью игнорируем API запросы - не перехватываем их
if (event.request.url.includes('/api/') || event.request.method !== 'GET') {
  return; // Не используем event.respondWith
}
```

**Что изменилось:**
- API запросы больше не перехватываются Service Worker
- Нет редиректов и CORS ошибок
- POST/PUT/DELETE запросы работают напрямую

## Как очистить кэш

**В браузере:**
1. Откройте DevTools (F12)
2. Application → Service Workers → Unregister
3. Application → Cache Storage → Clear storage
4. Жесткое обновление: Ctrl+Shift+R

**Или используйте режим инкогнито для тестирования**

## Проверьте

После очистки кэша:
1. ✅ Создание маршрутов
2. ✅ Создание задач
3. ✅ Создание заметок
4. ✅ Создание отпусков
5. ✅ Все POST/PUT/DELETE запросы

## Структура данных для тестирования

### Маршрут
```json
{
  "title": "Тестовый маршрут",
  "description": "Описание",
  "date": "2024-01-01T10:00",
  "assignee_ids": [1],
  "locations": [
    {"name": "Точка 1", "address": "Адрес 1", "order": 1}
  ]
}
```

### Задача
```json
{
  "title": "Тестовая задача",
  "description": "Описание",
  "priority": "medium",
  "deadline": "2024-01-01T10:00",
  "assignee_ids": [1],
  "tags": "тег1, тег2"
}
```

### Заметка
```json
{
  "title": "Тестовая заметка",
  "content": "Содержание",
  "category": "work",
  "tags": "тег1, тег2",
  "is_pinned": false
}
```

### Отпуск
```json
{
  "vacation_type": "vacation",
  "start_date": "2024-01-01",
  "end_date": "2024-01-10",
  "comment": "Комментарий"
}
```

Frontend перезапущен с исправлениями.
