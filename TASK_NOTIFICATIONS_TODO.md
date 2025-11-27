# 📋 Уведомления о задачах и фильтрация - План реализации

## ✅ ВЫПОЛНЕНО!

### 1. Уведомления при назначении задачи

#### Бэкенд:
- ✅ Добавить WebSocket событие `task_assigned`
- ✅ Отправлять уведомление при создании задачи с assignee
- ✅ Отправлять уведомление при изменении assignee

**Файлы для изменения:**
- ✅ `backend/app/api/tasks.py` - добавить отправку уведомления
- ✅ `backend/app/websocket/manager.py` - добавить метод `send_task_notification`
- ✅ `backend/app/schemas/task.py` - добавить TaskAssigneeResponse

#### Фронтенд:
- ✅ Подписаться на событие `task_assigned` в MainView или TasksView
- ✅ Показать браузерное уведомление
- ✅ Воспроизвести звук
- ✅ Обновить счетчик задач

**Файлы для изменения:**
- ✅ `frontend/src/views/TasksView.vue` - подписка на событие
- ✅ Использовать существующую систему звуков

### 2. Фильтрация назначенных задач

#### Фронтенд:
- ✅ Добавить вкладки/фильтры: "Все", "Назначенные мне", "Созданные мной"
- ✅ Добавить сортировку по статусу, дате, приоритету
- ✅ Сохранять выбранный фильтр в localStorage

**Файлы для изменения:**
- ✅ `frontend/src/views/TasksView.vue` - добавить UI фильтров

---

## 📄 Документация

- `TASK_NOTIFICATIONS_COMPLETE.md` - полное описание реализации
- `TASK_NOTIFICATIONS_TEST.md` - инструкции по тестированию
- `TASK_NOTIFICATIONS_SUMMARY.md` - краткое резюме

## 📝 Детальная реализация

### Шаг 1: Бэкенд - Уведомления

```python
# backend/app/api/tasks.py

@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # ... существующий код создания задачи ...
    
    # Отправляем уведомление назначенному пользователю
    if new_task.assigned_to:
        from app.websocket.manager import manager
        await manager.send_task_notification(
            user_id=new_task.assigned_to,
            task_id=new_task.id,
            task_title=new_task.title,
            assigned_by=current_user.id
        )
    
    return new_task
```

```python
# backend/app/websocket/manager.py

async def send_task_notification(self, user_id: int, task_id: int, task_title: str, assigned_by: int):
    """Отправка уведомления о назначении задачи"""
    message = {
        "type": "task_assigned",
        "task_id": task_id,
        "task_title": task_title,
        "assigned_by": assigned_by,
        "timestamp": datetime.utcnow().isoformat()
    }
    await self.send_personal_message(message, user_id)
```

### Шаг 2: Фронтенд - Подписка на уведомления

```javascript
// frontend/src/views/TasksView.vue или MainView.vue

import { useNotificationSounds } from '@/composables/useNotificationSounds'

const { playSound } = useNotificationSounds()

onMounted(() => {
  // Подписываемся на уведомления о задачах
  websocket.on('task_assigned', (data) => {
    // Показываем браузерное уведомление
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('Новая задача', {
        body: `Вам назначена задача: ${data.task_title}`,
        icon: '/logo.png'
      })
    }
    
    // Воспроизводим звук
    playSound()
    
    // Обновляем список задач
    loadTasks()
  })
})
```

### Шаг 3: Фронтенд - Фильтрация задач

```vue
<!-- frontend/src/views/TasksView.vue -->

<template>
  <div>
    <!-- Фильтры -->
    <div class="flex gap-2 mb-4">
      <button
        @click="filter = 'all'"
        :class="filter === 'all' ? 'btn-primary' : 'btn-secondary'"
      >
        Все ({{ allTasks.length }})
      </button>
      <button
        @click="filter = 'assigned'"
        :class="filter === 'assigned' ? 'btn-primary' : 'btn-secondary'"
      >
        Назначенные мне ({{ assignedToMe.length }})
      </button>
      <button
        @click="filter = 'created'"
        :class="filter === 'created' ? 'btn-primary' : 'btn-secondary'"
      >
        Созданные мной ({{ createdByMe.length }})
      </button>
    </div>
    
    <!-- Сортировка -->
    <select v-model="sortBy" class="mb-4">
      <option value="date">По дате</option>
      <option value="priority">По приоритету</option>
      <option value="status">По статусу</option>
    </select>
    
    <!-- Список задач -->
    <div v-for="task in filteredTasks" :key="task.id">
      <!-- ... -->
    </div>
  </div>
</template>

<script setup>
const filter = ref('all')
const sortBy = ref('date')
const currentUserId = authStore.user?.id

const assignedToMe = computed(() => 
  tasks.value.filter(t => t.assigned_to === currentUserId)
)

const createdByMe = computed(() => 
  tasks.value.filter(t => t.created_by === currentUserId)
)

const filteredTasks = computed(() => {
  let result = tasks.value
  
  // Фильтрация
  if (filter.value === 'assigned') {
    result = assignedToMe.value
  } else if (filter.value === 'created') {
    result = createdByMe.value
  }
  
  // Сортировка
  return result.sort((a, b) => {
    if (sortBy.value === 'date') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (sortBy.value === 'priority') {
      const priorities = { high: 3, medium: 2, low: 1 }
      return priorities[b.priority] - priorities[a.priority]
    } else if (sortBy.value === 'status') {
      return a.status.localeCompare(b.status)
    }
  })
})

// Сохранение фильтра
watch(filter, (newFilter) => {
  localStorage.setItem('taskFilter', newFilter)
})

onMounted(() => {
  filter.value = localStorage.getItem('taskFilter') || 'all'
})
</script>
```

## 🚀 Порядок реализации

1. **Бэкенд** - добавить WebSocket уведомления (30 мин)
2. **Фронтенд** - подписка на уведомления (15 мин)
3. **Фронтенд** - фильтрация и сортировка (30 мин)
4. **Тестирование** (15 мин)

## 📝 Примечания

- Используется существующая система звуков
- Используется существующий WebSocket
- Браузерные уведомления требуют разрешения пользователя
- Фильтр сохраняется в localStorage

## ✅ Готово к реализации

Все необходимые компоненты уже есть в системе:
- ✅ WebSocket работает
- ✅ Система звуков работает
- ✅ Notification API доступен
- ✅ localStorage используется

Нужно только связать все вместе!
