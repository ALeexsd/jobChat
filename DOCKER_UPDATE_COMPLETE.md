# Обновление Docker и исправление API

## Что было исправлено:

### 1. Маршруты (Routes)
**Проблема:** Фронтенд отправлял неправильную структуру данных
**Исправление:**
- Изменено `name` → `title`
- Изменено `start_date` → `date`
- Удалено `end_date` (не используется в API)
- Изменено `points: string[]` → `locations: {name, address, order}[]`
- Изменено `driver_id` → `assignee_ids: number[]`

**Структура данных:**
```json
{
  "title": "string",
  "description": "string",
  "date": "2024-01-01T00:00:00",
  "assignee_ids": [1, 2],
  "locations": [
    {
      "name": "Точка 1",
      "address": "Адрес 1",
      "order": 1
    }
  ]
}
```

### 2. Отпуска (Vacations)
**Проблема:** Неправильные названия полей
**Исправление:**
- Изменено `type` → `vacation_type`
- Изменено `reason` → `comment`

**Структура данных:**
```json
{
  "vacation_type": "vacation|sick_leave|personal",
  "start_date": "2024-01-01",
  "end_date": "2024-01-10",
  "comment": "string"
}
```

### 3. Задачи (Tasks)
**Проблема:** Неправильные поля и форматы
**Исправление:**
- Изменено `due_date` → `deadline` (ISO datetime)
- Изменено `assignee_id` → `assignee_ids: number[]`
- Изменено `tags: string[]` → `tags: string` (строка через запятую)
- Удалено поле `status` из формы создания (устанавливается автоматически)

**Структура данных:**
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high|urgent",
  "deadline": "2024-01-01T00:00:00",
  "assignee_ids": [1],
  "tags": "тег1, тег2, тег3"
}
```

### 4. Заметки (Notes)
**Проблема:** Лишнее поле и неправильный формат тегов
**Исправление:**
- Удалено поле `priority` (не используется в API)
- Изменено `tags: string[]` → `tags: string` (строка через запятую)

**Структура данных:**
```json
{
  "title": "string",
  "content": "string",
  "category": "work|personal|ideas|meetings|projects",
  "tags": "тег1, тег2, тег3",
  "is_pinned": false
}
```

## Обновленные компоненты:

1. ✅ `CreateRouteModal.vue` - исправлена структура данных
2. ✅ `CreateVacationModal.vue` - исправлены названия полей
3. ✅ `CreateTaskModal.vue` - исправлены поля и форматы
4. ✅ `CreateNoteModal.vue` - удалено лишнее поле, исправлены теги
5. ✅ `RoutesView.vue` - обновлено отображение данных (date, locations, status)
6. ✅ `VacationsView.vue` - обновлено отображение (vacation_type, comment)

## Docker контейнеры:

- ✅ Frontend перезапущен: `chat_frontend` (порт 3000)
- ✅ Backend работает: `chat_backend` (порт 8000)
- ✅ Database работает: `chat_postgres` (порт 5432)

## Проверьте:

1. Создание маршрутов - должно работать
2. Создание отпусков - должно работать
3. Создание задач - должно работать
4. Создание заметок - должно работать
5. Все формы корректно отображаются в светлой и темной теме

## Доступ:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
