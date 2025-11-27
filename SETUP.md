# Инструкция по установке и запуску

## Требования

- Docker и Docker Compose
- Node.js 18+ (для локальной разработки)
- Python 3.11+ (для локальной разработки)

## Быстрый старт с Docker

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Настройка переменных окружения

#### Backend
```bash
cd backend
cp .env.example .env
# Отредактируйте .env при необходимости
```

#### Frontend
```bash
cd frontend
cp .env.example .env
# Отредактируйте .env при необходимости
```

### 3. Запуск через Docker Compose

```bash
# Из корневой директории проекта
docker-compose up -d
```

Это запустит:
- PostgreSQL на порту 5432
- Backend API на порту 8000
- Frontend на порту 3000

### 4. Применение миграций

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Создание администратора

```bash
docker-compose exec backend python scripts/create_admin.py
```

Учетные данные по умолчанию:
- Username: `admin`
- Password: `admin123`

### 6. Доступ к приложению

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Локальная разработка без Docker

### Backend

```bash
cd backend

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
alembic upgrade head

# Создание админа
python scripts/create_admin.py

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm run dev
```

## Создание миграций

```bash
# Автоматическая генерация миграции
docker-compose exec backend alembic revision --autogenerate -m "migration message"

# Применение миграций
docker-compose exec backend alembic upgrade head

# Откат миграции
docker-compose exec backend alembic downgrade -1
```

## Остановка сервисов

```bash
docker-compose down

# С удалением volumes (БД будет очищена)
docker-compose down -v
```

## Логи

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## Тестирование

### Backend тесты

```bash
cd backend
pytest
```

## Структура проекта

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Конфигурация, безопасность, БД
│   │   ├── models/           # SQLAlchemy модели
│   │   ├── schemas/          # Pydantic схемы
│   │   ├── services/         # Бизнес-логика
│   │   ├── websocket/        # WebSocket handlers
│   │   └── main.py           # Точка входа
│   ├── alembic/              # Миграции БД
│   ├── scripts/              # Утилиты
│   ├── tests/                # Тесты
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── assets/           # Стили, изображения
│   │   ├── components/       # Vue компоненты
│   │   ├── router/           # Vue Router
│   │   ├── services/         # API и WebSocket сервисы
│   │   ├── stores/           # Pinia stores
│   │   ├── views/            # Страницы
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Troubleshooting

### Проблемы с подключением к БД

Убедитесь, что PostgreSQL запущен и доступен:
```bash
docker-compose ps
```

### Проблемы с миграциями

Пересоздайте БД:
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

### Проблемы с WebSocket

Проверьте, что в `.env` frontend правильно указан `VITE_WS_URL`

## Дополнительная информация

- FastAPI документация: https://fastapi.tiangolo.com/
- Vue.js документация: https://vuejs.org/
- Pinia документация: https://pinia.vuejs.org/
- SQLAlchemy документация: https://docs.sqlalchemy.org/
