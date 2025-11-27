# Исправление функции "Назначить задачу"

## Проблема
Кнопка "Назначить задачу" в профиле пользователя показывала alert "Функция в разработке".

## Решение

### 1. UserProfileView.vue
Функция `createTask` теперь перенаправляет на страницу задач с параметром assignee:
```javascript
function createTask() {
  router.push({
    path: '/tasks',
    query: { assignee: user.value.id }
  })
}
```

### 2. TasksView.vue
Добавлена поддержка query параметра `assignee`:
- При монтировании проверяется наличие параметра
- Если параметр есть, автоматически открывается модальное окно создания задачи
- Параметр передается в CreateTaskModal как `preselectedAssignee`

```javascript
onMounted(() => {
  loadTasks()
  
  if (route.query.assignee) {
    preselectedAssignee.value = parseInt(route.query.assignee)
    showCreateModal.value = true
  }
})
```

### 3. CreateTaskModal.vue
Добавлен новый prop `preselectedAssignee`:
- Принимает ID пользователя
- Автоматически устанавливает исполнителя при открытии модального окна

```javascript
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  preselectedAssignee: {
    type: Number,
    default: null
  }
})
```

## Как работает

1. Пользователь открывает профиль другого пользователя
2. Нажимает кнопку "Назначить задачу"
3. Перенаправляется на `/tasks?assignee=USER_ID`
4. Автоматически открывается модальное окно создания задачи
5. Поле "Исполнитель" уже заполнено выбранным пользователем
6. Пользователь заполняет остальные поля и создает задачу

## Проверьте

1. Откройте профиль любого пользователя (Сотрудники → выбрать пользователя)
2. Нажмите "Назначить задачу"
3. Должно открыться модальное окно с предзаполненным исполнителем
4. Заполните остальные поля и создайте задачу

Frontend перезапущен с исправлениями.
