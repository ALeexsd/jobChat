# 🎨 Tailwind CSS + Headless UI - Корпоративный мессенджер

## ✨ Обзор

Современное веб-приложение для корпоративного общения, построенное на **Vue 3**, **Tailwind CSS** и **Headless UI**.

---

## 🚀 Быстрый старт

```bash
# Запуск
docker-compose up -d

# Открыть приложение
http://localhost:3000
```

---

## 🛠️ Технологический стек

### Frontend
- **Vue 3** - Progressive JavaScript Framework
- **Tailwind CSS 3.3** - Utility-first CSS framework
- **Headless UI 1.7** - Unstyled, accessible UI components
- **Heroicons 2.1** - Beautiful hand-crafted SVG icons
- **Pinia** - State management
- **Vue Router** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL 15** - Database
- **JWT** - Authentication
- **Alembic** - Database migrations

---

## 📁 Структура проекта

```
ch2/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css          # Tailwind + кастомные классы
│   │   ├── components/
│   │   │   ├── CreateChatModal.vue
│   │   │   ├── CreateTaskModal.vue
│   │   │   └── CreateNoteModal.vue
│   │   ├── views/
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── MainView.vue
│   │   │   ├── ChatsView.vue
│   │   │   ├── ChatDetailView.vue
│   │   │   ├── TasksView.vue
│   │   │   ├── NotesView.vue
│   │   │   ├── VacationsView.vue
│   │   │   ├── RoutesView.vue
│   │   │   └── ProfileView.vue
│   │   ├── router/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── App.vue
│   │   └── main.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── package.json
│
├── backend/
│   └── app/
│
├── docker-compose.yml
└── README_TAILWIND.md
```

---

## 🎨 Дизайн система

### Цветовая палитра

**Primary (Фиолетовый):**
```
50:  #f5f3ff
500: #8b5cf6
600: #7c3aed  ← Основной
700: #6d28d9
```

### Кастомные классы

```css
.btn-primary    /* Основная кнопка */
.btn-secondary  /* Вторичная кнопка */
.card           /* Карточка */
.input          /* Поле ввода */
```

### Использование

```vue
<button class="btn-primary">Сохранить</button>
<div class="card p-6">Контент</div>
<input class="input" placeholder="Текст" />
```

---

## 📱 Адаптивность

Все компоненты адаптивны:

```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 1 колонка на mobile, 2 на tablet, 3 на desktop -->
</div>
```

**Breakpoints:**
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

---

## 🎭 Headless UI компоненты

### Dialog (Модальное окно)
```vue
<Dialog :open="isOpen" @close="closeModal">
  <DialogPanel class="card p-6">
    <DialogTitle>Заголовок</DialogTitle>
    <!-- Контент -->
  </DialogPanel>
</Dialog>
```

### Menu (Dropdown)
```vue
<Menu>
  <MenuButton>Меню</MenuButton>
  <MenuItems>
    <MenuItem>Пункт 1</MenuItem>
  </MenuItems>
</Menu>
```

### Listbox (Select)
```vue
<Listbox v-model="selected">
  <ListboxButton>{{ selected.name }}</ListboxButton>
  <ListboxOptions>
    <ListboxOption :value="item">
      {{ item.name }}
    </ListboxOption>
  </ListboxOptions>
</Listbox>
```

---

## 🎯 Основные функции

### 💬 Чаты
- Личные и групповые чаты
- Текстовые сообщения
- Изображения и файлы
- Голосовые сообщения
- Реакции (эмодзи)
- Ответы на сообщения

### ✅ Задачи
- Создание задач
- Приоритеты и статусы
- Назначение исполнителей
- Дедлайны
- Теги
- Фильтрация и поиск

### 📝 Заметки
- Создание заметок
- Категории
- Приоритеты
- Теги
- Закрепление
- Поиск

### 🏖️ Отпуска
- Подача заявлений
- Типы: отпуск, больничный, отгул
- Статусы
- Отмена заявлений

### 🗺️ Маршруты
- Создание маршрутов
- Точки маршрута
- Дата и время
- Начало маршрута

### 👤 Профиль
- Редактирование информации
- Изменение пароля
- Аватар с инициалами

---

## 🔧 Команды

### Docker
```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Логи
docker-compose logs -f frontend
```

### Frontend
```bash
# Установка зависимостей
docker-compose exec frontend npm install

# Добавить пакет
docker-compose exec frontend npm install [package]
```

### Backend
```bash
# Миграции
docker-compose exec backend alembic upgrade head

# Создать миграцию
docker-compose exec backend alembic revision --autogenerate -m "description"
```

---

## 📚 Документация

### Файлы документации:

1. **TAILWIND_DESIGN.md**
   - Полная документация по дизайну
   - Все компоненты с примерами
   - Utility классы

2. **QUICK_START.md**
   - Быстрый старт
   - Основные функции
   - Решение проблем

3. **MIGRATION_SUMMARY.md**
   - Детали миграции
   - Сравнение до/после
   - Преимущества

4. **TAILWIND_MIGRATION_COMPLETE.md**
   - Краткая сводка
   - Примеры использования
   - Советы по разработке

---

## 🔗 Ссылки

### Приложение
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Документация
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Headless UI](https://headlessui.com/)
- [Heroicons](https://heroicons.com/)
- [Vue 3](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## 📊 Производительность

### Размер бандла

**До (Ant Design):**
- ~700KB (gzipped)

**После (Tailwind + Headless UI):**
- ~30-40KB (gzipped)

**Экономия: ~95%** 🎉

---

## ✅ Особенности

- ✅ Современный utility-first CSS
- ✅ Полностью адаптивный дизайн
- ✅ Доступность (a11y) из коробки
- ✅ Легкий вес (~95% меньше CSS)
- ✅ Быстрая загрузка
- ✅ Легко кастомизировать
- ✅ Красивые анимации
- ✅ Темная тема (готово к добавлению)

---

## 🎉 Готово к использованию!

Откройте http://localhost:3000 и начните работу!

**Приятной разработки!** 🚀
