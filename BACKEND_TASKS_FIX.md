# Исправление API задач на бэкенде

## Проблема
При создании и обновлении задач возникала ошибка:
```
ResponseValidationError: Error extracting attribute: MissingGreenlet
```

Причина: SQLAlchemy пыталась загрузить связанные данные (subtasks, comments) вне async контекста.

## Решение

### 1. Исправлен POST /api/tasks/
**Было:**
```python
await db.commit()
await db.refresh(new_task)
return new_task
```

**Стало:**
```python
await db.commit()

# Загружаем задачу со всеми связанными данными
result = await db.execute(
    select(Task)
    .options(selectinload(Task.subtasks), selectinload(Task.comments))
    .where(Task.id == new_task.id)
)
task = result.scalar_one()

return task
```

### 2. Исправлен PUT/PATCH /api/tasks/{task_id}
**Было:**
```python
await db.commit()
await db.refresh(task)
return task
```

**Стало:**
```python
await db.commit()

# Загружаем задачу со всеми связанными данными
result = await db.execute(
    select(Task)
    .options(selectinload(Task.subtasks), selectinload(Task.comments))
    .where(Task.id == task_id)
)
task = result.scalar_one()

return task
```

### 3. Добавлена поддержка PATCH метода
```python
@router.put("/{task_id}", response_model=TaskResponse)
@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(...):
    ...
```

## Почему это важно

### Проблема с db.refresh()
`db.refresh()` не загружает связанные данные (relationships) автоматически в async режиме. Когда Pydantic пытается сериализовать ответ, он обращается к `task.subtasks` и `task.comments`, что вызывает lazy loading вне async контекста.

### Решение с selectinload
`selectinload()` явно загружает связанные данные в async режиме:
- Выполняет отдельный SELECT запрос для связанных данных
- Загружает все данные в async контексте
- Pydantic может безопасно сериализовать результат

## Что теперь работает

1. ✅ Создание задач (POST /api/tasks/)
2. ✅ Обновление задач (PUT /api/tasks/{id}/)
3. ✅ Частичное обновление (PATCH /api/tasks/{id}/)
4. ✅ Получение списка задач (GET /api/tasks/)
5. ✅ Получение одной задачи (GET /api/tasks/{id}/)
6. ✅ Нет CORS ошибок
7. ✅ Корректная сериализация с subtasks и comments

## Проверьте

1. Создайте новую задачу
2. Отредактируйте существующую задачу
3. Проверьте, что нет ошибок в логах бэкенда
4. Убедитесь, что задачи отображаются в списке

Backend перезапущен с исправлениями.
