# 🎨 Tailwind CSS + Headless UI - Полное обновление дизайна

## ✅ Что сделано:

### 1. Установка и настройка

#### Зависимости
```json
{
  "dependencies": {
    "@headlessui/vue": "^1.7.16",  // Headless UI компоненты
    "@heroicons/vue": "^2.1.1",    // Иконки
    "axios": "^1.6.2",
    "pinia": "^2.1.7",
    "vue": "^3.3.8",
    "vue-router": "^4.2.5"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6"        // Tailwind CSS
  }
}
```

#### Конфигурация Tailwind
```js
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f3ff',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
        }
      }
    }
  }
}
```

#### CSS файл
```css
/* src/assets/main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200;
  }
  
  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500;
  }
}
```

---

## 📁 Структура компонентов

### Views (Представления)

#### 1. **LoginView.vue** - Страница входа
```vue
<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-600">
  <div class="card p-8">
    <input class="input" />
    <button class="btn-primary">Войти</button>
  </div>
</div>
```

**Особенности:**
- Градиентный фон
- Центрированная форма
- Адаптивный дизайн

#### 2. **RegisterView.vue** - Регистрация
```vue
<div class="grid grid-cols-2 gap-4">
  <input class="input" />
</div>
```

**Особенности:**
- Grid layout для полей
- Валидация форм
- Responsive дизайн

#### 3. **MainView.vue** - Главный layout
```vue
<div class="h-screen flex">
  <!-- Sidebar -->
  <div :class="['bg-white border-r', sidebarCollapsed ? 'w-16' : 'w-64']">
    <nav>
      <router-link active-class="bg-primary-50 text-primary-600">
        <component :is="icon" class="w-6 h-6" />
      </router-link>
    </nav>
    
    <!-- User Menu -->
    <Menu as="div">
      <MenuButton>...</MenuButton>
      <MenuItems>...</MenuItems>
    </Menu>
  </div>
  
  <!-- Main Content -->
  <div class="flex-1 flex flex-col">
    <header class="h-16 bg-white border-b">
      <Menu as="div"><!-- Notifications --></Menu>
    </header>
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</div>
```

**Компоненты Headless UI:**
- `Menu` - Выпадающие меню
- `MenuButton` - Кнопка меню
- `MenuItems` - Список элементов
- `MenuItem` - Элемент меню

**Особенности:**
- Сворачиваемый sidebar
- Dropdown меню с анимацией
- Уведомления
- Активные ссылки

#### 4. **ChatsView.vue** - Список чатов
```vue
<div class="h-full flex flex-col p-6">
  <!-- Search -->
  <div class="relative">
    <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2" />
    <input class="w-full pl-10 input" />
  </div>
  
  <!-- Chats List -->
  <router-link class="card p-4 hover:shadow-md transition-shadow">
    <div class="flex items-center">
      <div class="w-12 h-12 rounded-full bg-primary-600">...</div>
      <div class="ml-4 flex-1">
        <h3 class="font-semibold">{{ chat.name }}</h3>
        <p class="text-sm text-gray-600">{{ chat.last_message }}</p>
      </div>
      <span class="px-2 py-1 bg-primary-600 text-white text-xs rounded-full">
        {{ chat.unread_count }}
      </span>
    </div>
  </router-link>
</div>
```

**Особенности:**
- Поиск с иконкой
- Карточки чатов
- Счетчик непрочитанных
- Hover эффекты

#### 5. **ChatDetailView.vue** - Детали чата
```vue
<div class="h-full flex flex-col">
  <!-- Header -->
  <div class="bg-white border-b px-6 py-4">
    <Menu as="div"><!-- Actions --></Menu>
  </div>
  
  <!-- Messages -->
  <div class="flex-1 overflow-y-auto p-6 space-y-4">
    <div :class="['flex', message.sender_id === currentUserId ? 'justify-end' : 'justify-start']">
      <div :class="[
        'max-w-md px-4 py-2 rounded-2xl',
        message.sender_id === currentUserId
          ? 'bg-primary-600 text-white rounded-br-sm'
          : 'bg-white text-gray-900 rounded-bl-sm'
      ]">
        {{ message.content }}
      </div>
    </div>
  </div>
  
  <!-- Input -->
  <div class="bg-white border-t p-4">
    <div class="flex items-center space-x-2">
      <button class="p-2 hover:bg-gray-100 rounded-lg">
        <PhotoIcon class="w-6 h-6" />
      </button>
      <input class="flex-1 input" />
      <button class="btn-primary">
        <PaperAirplaneIcon class="w-5 h-5" />
      </button>
    </div>
  </div>
</div>
```

**Особенности:**
- Bubble-стиль сообщений
- Разные цвета для своих/чужих
- Прикрепление файлов
- Emoji picker

#### 6. **TasksView.vue** - Задачи
```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card p-4 hover:shadow-md transition-shadow">
    <span :class="['px-2 py-1 text-xs rounded', getPriorityClass(task.priority)]">
      {{ task.priority }}
    </span>
    
    <h3 class="text-lg font-semibold">{{ task.title }}</h3>
    <p class="text-sm text-gray-600 line-clamp-2">{{ task.description }}</p>
    
    <div class="flex flex-wrap gap-1">
      <span class="px-2 py-1 bg-gray-100 text-xs rounded">{{ tag }}</span>
    </div>
  </div>
</div>
```

**Особенности:**
- Grid layout (адаптивный)
- Цветные бейджи приоритетов
- Line clamp для текста
- Теги

#### 7. **NotesView.vue** - Заметки
```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <div class="card p-4 relative">
    <div v-if="note.is_pinned" class="absolute top-2 right-2">
      <StarIcon class="w-5 h-5 text-yellow-500 fill-current" />
    </div>
    <h3 class="text-lg font-semibold pr-6">{{ note.title }}</h3>
    <p class="text-sm text-gray-600 line-clamp-3">{{ note.content }}</p>
  </div>
</div>
```

**Особенности:**
- 4-колоночный grid
- Закрепленные заметки
- Line clamp для превью

#### 8. **VacationsView.vue** - Отпуска
```vue
<table class="w-full">
  <thead class="bg-gray-50 sticky top-0">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
        Тип
      </th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    <tr class="hover:bg-gray-50">
      <td class="px-6 py-4">
        <span :class="['px-2 py-1 text-xs rounded', getTypeClass(vacation.type)]">
          {{ vacation.type }}
        </span>
      </td>
    </tr>
  </tbody>
</table>
```

**Особенности:**
- Sticky header
- Hover эффекты на строках
- Цветные статусы

#### 9. **RoutesView.vue** - Маршруты
```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card p-4">
    <div class="flex items-start justify-between">
      <TruckIcon class="w-6 h-6 text-primary-600" />
      <Menu as="div"><!-- Actions --></Menu>
    </div>
    
    <div class="space-y-1">
      <div class="flex items-start">
        <MapPinIcon class="w-4 h-4 mr-2 flex-shrink-0" />
        <span>{{ point.address }}</span>
      </div>
    </div>
    
    <div class="flex space-x-2">
      <button class="flex-1 btn-primary">Начать</button>
      <button class="flex-1 btn-secondary">На карте</button>
    </div>
  </div>
</div>
```

**Особенности:**
- Карточки маршрутов
- Список точек с иконками
- Кнопки действий

#### 10. **ProfileView.vue** - Профиль
```vue
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <!-- Avatar Card -->
  <div class="card p-6">
    <div class="w-24 h-24 rounded-full bg-primary-600 mx-auto">
      {{ userInitials }}
    </div>
  </div>
  
  <!-- Info Card -->
  <div class="lg:col-span-2">
    <div class="card p-6">
      <form class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <input class="input" />
        </div>
      </form>
    </div>
  </div>
</div>
```

**Особенности:**
- Grid layout
- Аватар с инициалами
- Формы редактирования

---

## 🎭 Модальные окна (Headless UI)

### CreateChatModal.vue
```vue
<TransitionRoot appear :show="show">
  <Dialog @close="$emit('close')">
    <TransitionChild>
      <div class="fixed inset-0 bg-black bg-opacity-25" />
    </TransitionChild>
    
    <div class="fixed inset-0 overflow-y-auto">
      <TransitionChild>
        <DialogPanel class="w-full max-w-md rounded-2xl bg-white p-6">
          <DialogTitle>Создать чат</DialogTitle>
          
          <Listbox v-model="formData.members" multiple>
            <ListboxButton class="input">...</ListboxButton>
            <ListboxOptions>
              <ListboxOption v-slot="{ active, selected }">
                <CheckIcon v-if="selected" />
              </ListboxOption>
            </ListboxOptions>
          </Listbox>
        </DialogPanel>
      </TransitionChild>
    </div>
  </Dialog>
</TransitionRoot>
```

**Компоненты:**
- `Dialog` - Модальное окно
- `DialogPanel` - Панель диалога
- `DialogTitle` - Заголовок
- `Listbox` - Выпадающий список
- `TransitionRoot/Child` - Анимации

---

## 🎨 Utility классы Tailwind

### Layout
```css
.h-screen          /* height: 100vh */
.flex              /* display: flex */
.flex-col          /* flex-direction: column */
.items-center      /* align-items: center */
.justify-between   /* justify-content: space-between */
.space-x-4         /* gap между элементами по X */
.space-y-4         /* gap между элементами по Y */
```

### Sizing
```css
.w-full            /* width: 100% */
.w-64              /* width: 16rem */
.h-16              /* height: 4rem */
.max-w-md          /* max-width: 28rem */
```

### Colors
```css
.bg-primary-600    /* background: #7c3aed */
.text-white        /* color: white */
.text-gray-900     /* color: #111827 */
.border-gray-200   /* border-color: #e5e7eb */
```

### Typography
```css
.text-sm           /* font-size: 0.875rem */
.text-lg           /* font-size: 1.125rem */
.font-semibold     /* font-weight: 600 */
.truncate          /* text-overflow: ellipsis */
.line-clamp-2      /* ограничение строк */
```

### Spacing
```css
.p-4               /* padding: 1rem */
.px-6              /* padding-left/right: 1.5rem */
.py-4              /* padding-top/bottom: 1rem */
.m-4               /* margin: 1rem */
.mb-6              /* margin-bottom: 1.5rem */
```

### Borders & Shadows
```css
.rounded-lg        /* border-radius: 0.5rem */
.rounded-full      /* border-radius: 9999px */
.shadow-sm         /* box-shadow: small */
.shadow-lg         /* box-shadow: large */
.border            /* border: 1px solid */
```

### Effects
```css
.hover:bg-gray-100      /* hover эффект */
.transition-colors      /* плавный переход цветов */
.opacity-50            /* opacity: 0.5 */
```

### Responsive
```css
.md:grid-cols-2    /* @media (min-width: 768px) */
.lg:grid-cols-3    /* @media (min-width: 1024px) */
.xl:grid-cols-4    /* @media (min-width: 1280px) */
```

---

## 🎯 Преимущества Tailwind CSS

### 1. **Utility-First подход**
- Быстрая разработка
- Нет необходимости придумывать имена классов
- Все стили в одном месте

### 2. **Адаптивность из коробки**
```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <!-- Автоматически адаптируется -->
</div>
```

### 3. **Темизация**
```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: { /* ваши цвета */ }
    }
  }
}
```

### 4. **Оптимизация**
- PurgeCSS удаляет неиспользуемые стили
- Минимальный размер финального CSS

### 5. **Консистентность**
- Единая система отступов
- Согласованные цвета
- Стандартные размеры

---

## 🚀 Headless UI преимущества

### 1. **Доступность (a11y)**
- Keyboard navigation
- Screen reader support
- ARIA attributes

### 2. **Гибкость**
- Полный контроль над стилями
- Нет предустановленного дизайна

### 3. **Анимации**
```vue
<TransitionChild
  enter="duration-300 ease-out"
  enter-from="opacity-0 scale-95"
  enter-to="opacity-100 scale-100"
>
```

### 4. **Компоненты**
- Menu (Dropdown)
- Dialog (Modal)
- Listbox (Select)
- Combobox (Autocomplete)
- Switch (Toggle)
- Tabs
- Disclosure (Accordion)

---

## 📦 Иконки (@heroicons/vue)

### Использование
```vue
<script setup>
import {
  ChatBubbleLeftRightIcon,
  UserCircleIcon,
  BellIcon
} from '@heroicons/vue/24/outline'  // outline стиль

import {
  CheckIcon,
  StarIcon
} from '@heroicons/vue/24/solid'    // solid стиль
</script>

<template>
  <ChatBubbleLeftRightIcon class="w-6 h-6 text-gray-600" />
</template>
```

### Доступные иконки
- 200+ иконок
- Outline и Solid варианты
- SVG формат
- Легко кастомизируются

---

## 🎨 Кастомные компоненты

### Button
```css
.btn-primary {
  @apply bg-primary-600 text-white px-4 py-2 rounded-lg 
         hover:bg-primary-700 transition-colors 
         disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-900 px-4 py-2 rounded-lg 
         hover:bg-gray-300 transition-colors;
}
```

### Card
```css
.card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200;
}
```

### Input
```css
.input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg 
         focus:outline-none focus:ring-2 focus:ring-primary-500 
         focus:border-transparent;
}
```

---

## 🔧 Запуск проекта

```bash
# Установка зависимостей
docker-compose exec frontend npm install

# Перезапуск контейнера
docker-compose restart frontend

# Проверка
http://localhost:5173
```

---

## ✅ Итог

Весь дизайн переписан на **Tailwind CSS + Headless UI**:
- ✅ Все views обновлены
- ✅ Все модальные окна с Headless UI
- ✅ Адаптивный дизайн
- ✅ Современные анимации
- ✅ Доступность (a11y)
- ✅ Оптимизированный CSS
- ✅ Консистентный UI

Дизайн готов к использованию! 🎉
