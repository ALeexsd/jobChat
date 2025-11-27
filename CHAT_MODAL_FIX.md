# Исправление выпадающего списка в CreateChatModal

## Проблема
Выпадающий список участников (Listbox от Headless UI) отображался некорректно:
- Текст накладывался друг на друга
- Плохая читаемость
- Неудобный интерфейс

## Решение

Заменил Listbox на простые списки с чекбоксами и кнопками.

### Для группового чата
**Было:** Listbox с множественным выбором
**Стало:** Список с чекбоксами

```vue
<div class="border rounded-lg max-h-60 overflow-y-auto">
  <div
    v-for="user in users"
    :key="user.id"
    class="flex items-center p-3 hover:bg-gray-50 cursor-pointer"
    @click="toggleMember(user.id)"
  >
    <input type="checkbox" :checked="formData.members.includes(user.id)" />
    <div class="ml-3">
      <p>{{ user.first_name }} {{ user.last_name }}</p>
      <p class="text-xs">@{{ user.username }}</p>
    </div>
  </div>
</div>
```

**Преимущества:**
- ✅ Четкое отображение всех пользователей
- ✅ Видно, кто выбран (чекбокс)
- ✅ Счетчик выбранных участников
- ✅ Клик по всей строке для выбора

### Для личного чата
**Было:** Listbox с одиночным выбором
**Стало:** Список кнопок с аватарами

```vue
<div class="border rounded-lg max-h-60 overflow-y-auto">
  <button
    v-for="user in users"
    :key="user.id"
    @click="formData.user = user.id"
    class="w-full flex items-center p-3"
  >
    <div class="avatar">...</div>
    <div class="ml-3">
      <p>{{ user.first_name }} {{ user.last_name }}</p>
      <p class="text-xs">@{{ user.username }}</p>
    </div>
    <CheckIcon v-if="formData.user === user.id" />
  </button>
</div>
```

**Преимущества:**
- ✅ Отображение аватаров пользователей
- ✅ Визуальная индикация выбранного пользователя (CheckIcon)
- ✅ Hover эффекты
- ✅ Лучшая читаемость

## Изменения в коде

### Добавлена функция toggleMember
```javascript
function toggleMember(userId) {
  const index = formData.value.members.indexOf(userId)
  if (index > -1) {
    formData.value.members.splice(index, 1)
  } else {
    formData.value.members.push(userId)
  }
}
```

### Удалены неиспользуемые импорты
- Listbox
- ListboxButton
- ListboxOptions
- ListboxOption
- getUserLabel (функция)

### Обновлены стили
- Темная тема полностью поддерживается
- Hover эффекты для лучшего UX
- Скроллбар для длинных списков
- Фиксированная высота (max-h-60)

## Проверьте

1. ✅ Создание группового чата - выбор нескольких участников
2. ✅ Создание личного чата - выбор одного пользователя
3. ✅ Отображение аватаров
4. ✅ Счетчик выбранных участников
5. ✅ Работа в темной теме
6. ✅ Hover эффекты

Frontend перезапущен с исправлениями.
