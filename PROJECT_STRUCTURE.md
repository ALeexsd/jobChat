# Структура проекта

Полная структура корпоративного мессенджера с описанием каждого файла и директории.

```
corporate-messenger/
│
├── 📁 backend/                          # Backend приложение (FastAPI)
│   ├── 📁 app/                          # Основной код приложения
│   │   ├── 📁 api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                  # Аутентификация (login, register, refresh)
│   │   │   ├── users.py                 # Управление пользователями
│   │   │   ├── chats.py                 # Управление чатами
│   │   │   ├── messages.py              # Сообщения и файлы
│   │   │   ├── tasks.py                 # Управление задачами
│   │   │   ├── routes.py                # Маршруты
│   │   │   ├── notes.py                 # Заметки
│   │   │   ├── vacations.py             # Отпуска
│   │   │   └── notifications.py         # Уведомления
│   │   │
│   │   ├── 📁 core/                     # Ядро приложения
│   │   │   ├── __init__.py
│   │   │   ├── config.py                # Конфигурация (settings)
│   │   │   ├── database.py              # Подключение к БД
│   │   │   └── security.py              # JWT, хэширование паролей
│   │   │
│   │   ├── 📁 models/                   # SQLAlchemy модели
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # Модель пользователя
│   │   │   ├── chat.py                  # Модели чатов
│   │   │   ├── message.py               # Модели сообщений
│   │   │   ├── task.py                  # Модели задач
│   │   │   ├── route.py                 # Модели маршрутов
│   │   │   ├── note.py                  # Модель заметок
│   │   │   ├── vacation.py              # Модель отпусков
│   │   │   └── notification.py          # Модель уведомлений
│   │   │
│   │   ├── 📁 schemas/                  # Pydantic схемы
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # Схемы пользователя
│   │   │   ├── chat.py                  # Схемы чатов
│   │   │   ├── message.py               # Схемы сообщений
│   │   │   ├── task.py                  # Схемы задач
│   │   │   ├── route.py                 # Схемы маршрутов
│   │   │   ├── note.py                  # Схемы заметок
│   │   │   ├── vacation.py              # Схемы отпусков
│   │   │   └── notification.py          # Схемы уведомлений
│   │   │
│   │   ├── 📁 websocket/                # WebSocket обработчики
│   │   │   ├── __init__.py
│   │   │   └── manager.py               # Connection manager
│   │   │
│   │   ├── __init__.py
│   │   └── main.py                      # Точка входа FastAPI
│   │
│   ├── 📁 alembic/                      # Миграции БД
│   │   ├── versions/                    # Файлы миграций
│   │   ├── env.py                       # Конфигурация Alembic
│   │   └── script.py.mako               # Шаблон миграций
│   │
│   ├── 📁 scripts/                      # Утилиты и скрипты
│   │   └── create_admin.py              # Создание администратора
│   │
│   ├── 📁 tests/                        # Тесты
│   │   ├── __init__.py
│   │   ├── test_auth.py                 # Тесты аутентификации
│   │   ├── test_users.py                # Тесты пользователей
│   │   ├── test_chats.py                # Тесты чатов
│   │   └── test_tasks.py                # Тесты задач
│   │
│   ├── 📁 media/                        # Загруженные файлы (создается автоматически)
│   │
│   ├── .env.example                     # Пример переменных окружения
│   ├── .gitignore                       # Git ignore файл
│   ├── alembic.ini                      # Конфигурация Alembic
│   ├── Dockerfile                       # Docker образ для разработки
│   ├── Dockerfile.prod                  # Docker образ для production
│   ├── pytest.ini                       # Конфигурация pytest
│   └── requirements.txt                 # Python зависимости
│
├── 📁 frontend/                         # Frontend приложение (Vue.js 3)
│   ├── 📁 public/                       # Статические файлы
│   │   └── favicon.ico
│   │
│   ├── 📁 src/                          # Исходный код
│   │   ├── 📁 assets/                   # Ресурсы
│   │   │   ├── 📁 images/               # Изображения
│   │   │   └── 📁 styles/               # Стили
│   │   │       └── main.scss            # Основные стили
│   │   │
│   │   ├── 📁 components/               # Vue компоненты
│   │   │   ├── ChatList.vue             # Список чатов
│   │   │   ├── MessageItem.vue          # Элемент сообщения
│   │   │   ├── TaskCard.vue             # Карточка задачи
│   │   │   ├── UserAvatar.vue           # Аватар пользователя
│   │   │   └── NotificationBell.vue     # Колокольчик уведомлений
│   │   │
│   │   ├── 📁 router/                   # Vue Router
│   │   │   └── index.js                 # Конфигурация маршрутов
│   │   │
│   │   ├── 📁 services/                 # Сервисы
│   │   │   ├── api.js                   # HTTP клиент (Axios)
│   │   │   └── websocket.js             # WebSocket клиент
│   │   │
│   │   ├── 📁 stores/                   # Pinia stores
│   │   │   ├── auth.js                  # Store аутентификации
│   │   │   ├── chat.js                  # Store чатов
│   │   │   └── task.js                  # Store задач
│   │   │
│   │   ├── 📁 views/                    # Страницы (views)
│   │   │   ├── LoginView.vue            # Страница входа
│   │   │   ├── RegisterView.vue         # Страница регистрации
│   │   │   ├── MainView.vue             # Главная страница с навигацией
│   │   │   ├── ChatsView.vue            # Список чатов
│   │   │   ├── ChatDetailView.vue       # Детали чата
│   │   │   ├── TasksView.vue            # Список задач
│   │   │   ├── RoutesView.vue           # Маршруты
│   │   │   ├── NotesView.vue            # Заметки
│   │   │   ├── VacationsView.vue        # Отпуска
│   │   │   ├── BirthdaysView.vue        # Дни рождения
│   │   │   └── ProfileView.vue          # Профиль пользователя
│   │   │
│   │   ├── App.vue                      # Корневой компонент
│   │   └── main.js                      # Точка входа
│   │
│   ├── .env.example                     # Пример переменных окружения
│   ├── .gitignore                       # Git ignore файл
│   ├── Dockerfile                       # Docker образ для разработки
│   ├── Dockerfile.prod                  # Docker образ для production
│   ├── index.html                       # HTML шаблон
│   ├── package.json                     # NPM зависимости
│   └── vite.config.js                   # Конфигурация Vite
│
├── 📁 nginx/                            # Nginx конфигурация
│   ├── nginx.conf                       # Основная конфигурация
│   ├── frontend.conf                    # Конфигурация для frontend
│   └── 📁 ssl/                          # SSL сертификаты
│
├── 📁 docs/                             # Дополнительная документация
│   ├── api/                             # API документация
│   ├── guides/                          # Руководства
│   └── screenshots/                     # Скриншоты
│
├── 📄 .env.example                      # Пример переменных окружения (общий)
├── 📄 .gitignore                        # Git ignore (корневой)
├── 📄 docker-compose.yml                # Docker Compose для разработки
├── 📄 docker-compose.prod.yml           # Docker Compose для production
│
├── 📄 README.md                         # Основная документация
├── 📄 SETUP.md                          # Инструкция по установке
├── 📄 ARCHITECTURE.md                   # Архитектура проекта
├── 📄 API_DOCUMENTATION.md              # API документация
├── 📄 FEATURES.md                       # Список функций
├── 📄 EXAMPLES.md                       # Примеры использования
├── 📄 DEPLOYMENT.md                     # Руководство по деплою
├── 📄 TODO.md                           # Список задач
├── 📄 PROJECT_STRUCTURE.md              # Этот файл
├── 📄 LICENSE                           # Лицензия MIT
└── 📄 CHANGELOG.md                      # История изменений

```

## 📝 Описание ключевых файлов

### Backend

#### `app/main.py`
Точка входа приложения. Создает FastAPI приложение, подключает роутеры, настраивает CORS и middleware.

#### `app/core/config.py`
Конфигурация приложения через Pydantic Settings. Загружает переменные окружения.

#### `app/core/database.py`
Настройка подключения к PostgreSQL через SQLAlchemy. Async engine и session maker.

#### `app/core/security.py`
Функции безопасности: хэширование паролей, создание JWT токенов, проверка токенов.

#### `app/models/*.py`
SQLAlchemy модели для всех сущностей. Определяют структуру таблиц БД.

#### `app/schemas/*.py`
Pydantic схемы для валидации входящих и исходящих данных.

#### `app/api/*.py`
REST API endpoints. Каждый файл отвечает за свою область (auth, users, chats и т.д.).

#### `app/websocket/manager.py`
WebSocket connection manager. Управляет подключениями, отправкой и получением сообщений.

### Frontend

#### `src/main.js`
Точка входа. Создает Vue приложение, подключает Pinia и Router.

#### `src/App.vue`
Корневой компонент. Содержит router-view и глобальные стили.

#### `src/router/index.js`
Конфигурация Vue Router. Определяет все маршруты и guards.

#### `src/stores/*.js`
Pinia stores для управления состоянием. Каждый store отвечает за свою область.

#### `src/services/api.js`
HTTP клиент на базе Axios. Настроены interceptors для токенов.

#### `src/services/websocket.js`
WebSocket клиент. Управляет подключением и обработкой сообщений.

#### `src/views/*.vue`
Страницы приложения. Каждая страница - отдельный route.

#### `src/components/*.vue`
Переиспользуемые компоненты. Используются в разных views.

### Конфигурация

#### `docker-compose.yml`
Конфигурация для разработки. Включает hot-reload и volume mounting.

#### `docker-compose.prod.yml`
Конфигурация для production. Оптимизирована для производительности.

#### `alembic.ini`
Конфигурация Alembic для миграций БД.

#### `vite.config.js`
Конфигурация Vite для сборки frontend.

### Документация

#### `README.md`
Основная документация проекта. Быстрый старт и обзор.

#### `SETUP.md`
Детальная инструкция по установке и настройке.

#### `ARCHITECTURE.md`
Описание архитектуры проекта, технологий и паттернов.

#### `API_DOCUMENTATION.md`
Полная документация API с примерами запросов.

#### `DEPLOYMENT.md`
Руководство по развертыванию в production.

## 🔍 Навигация по проекту

### Где найти...

**Модели БД**: `backend/app/models/`
**API endpoints**: `backend/app/api/`
**Схемы валидации**: `backend/app/schemas/`
**Vue компоненты**: `frontend/src/components/`
**Страницы**: `frontend/src/views/`
**State management**: `frontend/src/stores/`
**Стили**: `frontend/src/assets/styles/`
**Миграции БД**: `backend/alembic/versions/`
**Тесты**: `backend/tests/`
**Конфигурация**: корневая директория

## 📦 Размер проекта

Приблизительное количество строк кода:

- **Backend**: ~3,000 строк Python
- **Frontend**: ~2,500 строк JavaScript/Vue
- **Стили**: ~500 строк SCSS
- **Конфигурация**: ~500 строк YAML/JSON
- **Документация**: ~5,000 строк Markdown

**Всего**: ~11,500 строк кода

## 🎯 Точки входа

### Для разработчика Backend
1. `backend/app/main.py` - старт приложения
2. `backend/app/api/` - добавление новых endpoints
3. `backend/app/models/` - создание новых моделей
4. `backend/alembic/` - миграции БД

### Для разработчика Frontend
1. `frontend/src/main.js` - старт приложения
2. `frontend/src/views/` - создание новых страниц
3. `frontend/src/components/` - создание компонентов
4. `frontend/src/stores/` - управление состоянием

### Для DevOps
1. `docker-compose.yml` - разработка
2. `docker-compose.prod.yml` - production
3. `nginx/nginx.conf` - конфигурация веб-сервера
4. `DEPLOYMENT.md` - инструкции по деплою

## 🔄 Жизненный цикл запроса

### REST API запрос
```
Client → Nginx → Backend (FastAPI) → Database (PostgreSQL)
   ↑                                        ↓
   └────────────────────────────────────────┘
```

### WebSocket сообщение
```
Client ←→ Nginx ←→ Backend (WebSocket Manager) ←→ Other Clients
```

### Аутентификация
```
Client → Login → JWT Token → Store in localStorage → 
Include in Headers → Backend validates → Access granted
```

## 📚 Дополнительные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js 3 Documentation](https://vuejs.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Docker Documentation](https://docs.docker.com/)
