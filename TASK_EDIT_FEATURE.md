# Функция редактирования задач

## Проблема
Кнопка "Редактировать" в задачах только логировала данные в консоль, но не открывала модальное окно редактирования.

## Решение

Создан новый компонент **EditTaskModal.vue** с полным функционалом редактирования задач.

## Возможности EditTaskModal

### Редактируемые поля
- ✅ Название задачи
- ✅ Описание
- ✅ Приоритет (низкий, средний, высокий, срочный)
- ✅ Статус (к выполнению, в работе, на проверке, выполнено)
- ✅ Дедлайн (дата и время)
- ✅ Исполнитель (выбор из списка пользователей)
- ✅ Теги (добавление/удаление)

### Особенности
- ✅ Автозагрузка данных задачи при открытии
- ✅ Преобразование datetime для input type="datetime-local"
- ✅ Поддержка тегов (строка или массив)
- ✅ Валидация обязательных полей
- ✅ Обработка ошибок с понятными сообщениями
- ✅ Темная тема

### Интеграция с TasksView

```vue
<!-- Edit Task Modal -->
<EditTaskModal
  :show="showEditModal"
  :task="selectedTask"
  @close="showEditModal = false"
  @updated="handleTaskUpdated"
/>
```

### Обработчики
```javascript
function editTask(task) {
  selectedTask.value = task
  showEditModal.value = true
}

async function handleTaskUpdated() {
  await loadTasks() // Обновляем список задач
}
```

## API запрос

```javascript
PATCH /api/tasks/{task_id}/
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high|urgent",
  "status": "todo|in_progress|review|done",
  "deadline": "2024-01-01T10:00",
  "assignee_ids": [1],
  "tags": "тег1, тег2"
}
```

## Преобразование данных

### Загрузка задачи
```javascript
function loadTaskData() {
  formData.value = {
    title: props.task.title || '',
    description: props.task.description || '',
    priority: props.task.priority || 'medium',
    status: props.task.status || 'todo',
    deadline: props.task.deadline ? formatDatetimeLocal(props.task.deadline) : '',
    assignee: props.task.assignee_id || null,
    tags: parseTaskTags(props.task.tags)
  }
}
```

### Форматирование datetime
```javascript
function formatDatetimeLocal(datetime) {
  // Преобразует ISO datetime в формат для input type="datetime-local"
  // "2024-01-01T10:00:00Z" -> "2024-01-01T10:00"
}
```

### Обработка тегов
```javascript
// Поддержка как строки, так и массива
tags: props.task.tags ? 
  (typeof props.task.tags === 'string' ? 
    props.task.tags.split(',').map(t => t.trim()) : 
    props.task.tags
  ) : []
```

## Использование

### Открыть редактирование
1. Откройте страницу "Задачи"
2. Нажмите на меню задачи (три точки)
3. Выберите "Редактировать"
4. Модальное окно откроется с данными задачи

### Редактировать задачу
1. Измените нужные поля
2. Добавьте/удалите теги
3. Нажмите "Сохранить"
4. Список задач автоматически обновится

### Отменить изменения
1. Нажмите "Отмена" или закройте модальное окно
2. Изменения не сохранятся

## Дизайн

### Светлая тема
- Белый фон модального окна
- Четкие границы полей
- Синие акценты

### Темная тема
- Темно-серый фон (dark:bg-gray-800)
- Темные поля ввода (dark:bg-gray-700)
- Адаптированные цвета текста

## Проверьте

1. ✅ Открытие модального окна редактирования
2. ✅ Загрузка данных задачи
3. ✅ Редактирование всех полей
4. ✅ Изменение статуса задачи
5. ✅ Добавление/удаление тегов
6. ✅ Изменение исполнителя
7. ✅ Сохранение изменений
8. ✅ Обновление списка задач
9. ✅ Работа в темной теме

Frontend перезапущен с функцией редактирования задач.
