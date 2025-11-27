# 🐳 Запуск проекта в Docker

## ✅ Проект успешно запущен!

### 🎯 Запущенные сервисы:

1. **PostgreSQL** (chat_postgres)
   - Порт: 5432
   - База данных: chatdb
   - Пользователь: chatuser
   - Статус: ✅ Healthy

2. **Backend** (chat_backend)
   - Порт: 8000
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Статус: ✅ Running

3. **Frontend** (chat_frontend)
   - Порт: 3000
   - URL: http://localhost:3000
   - Статус: ✅ Running

## 🚀 Быстрый старт:

### Первый запуск:
```bash
# Остановить и удалить старые контейнеры
docker-compose down -v

# Собрать и запустить
docker-compose up -d --build

# Применить миграции БД
docker exec chat_backend alembic upgrade head
```

### Последующие запуски:
```bash
# Запустить
docker-compose up -d

# Остановить
docker-compose down
```

## 📊 Полезные команды:

### Просмотр логов:
```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только frontend
docker-compose logs -f frontend

# Последние 50 строк
docker-compose logs --tail=50 backend
```

### Статус контейнеров:
```bash
docker-compose ps
```

### Перезапуск сервиса:
```bash
# Перезапустить backend
docker-compose restart backend

# Перезапустить frontend
docker-compose restart frontend
```

### Выполнение команд внутри контейнера:
```bash
# Backend shell
docker exec -it chat_backend bash

# Frontend shell
docker exec -it chat_frontend sh

# PostgreSQL shell
docker exec -it chat_postgres psql -U chatuser -d chatdb
```

### Создание миграций:
```bash
# Создать новую миграцию
docker exec chat_backend alembic revision --autogenerate -m "описание изменений"

# Применить миграции
docker exec chat_backend alembic upgrade head

# Откатить миграцию
docker exec chat_backend alembic downgrade -1
```

## 🔧 Обновление кода:

### Backend:
```bash
# Код обновляется автоматически (volume mount)
# Uvicorn перезагружается при изменениях

# Если нужно пересобрать:
docker-compose up -d --build backend
```

### Frontend:
```bash
# Код обновляется автоматически (volume mount)
# Vite HMR работает

# Если нужно пересобрать:
docker-compose up -d --build frontend
```

## 🗄️ База данных:

### Подключение:
- Host: localhost
- Port: 5432
- Database: chatdb
- User: chatuser
- Password: chatpass

### Резервное копирование:
```bash
# Создать backup
docker exec chat_postgres pg_dump -U chatuser chatdb > backup.sql

# Восстановить backup
docker exec -i chat_postgres psql -U chatuser chatdb < backup.sql
```

## 🐛 Решение проблем:

### Backend не запускается:
```bash
# Проверить логи
docker-compose logs backend

# Пересобрать контейнер
docker-compose up -d --build backend

# Проверить переменные окружения
docker exec chat_backend env
```

### Frontend не запускается:
```bash
# Проверить логи
docker-compose logs frontend

# Переустановить зависимости
docker-compose down
docker volume rm ch2_frontend_node_modules
docker-compose up -d --build frontend
```

### База данных не доступна:
```bash
# Проверить статус
docker-compose ps postgres

# Проверить логи
docker-compose logs postgres

# Пересоздать базу
docker-compose down -v
docker-compose up -d postgres
```

### Порты заняты:
```bash
# Найти процесс на порту 8000
netstat -ano | findstr :8000

# Остановить процесс (замените PID)
taskkill /PID <PID> /F

# Или измените порты в docker-compose.yml
```

## 📁 Структура volumes:

- `ch2_postgres_data` - данные PostgreSQL
- `ch2_media_files` - загруженные файлы (фото, аудио)
- `node_modules` - зависимости frontend (анонимный volume)

## 🔄 Полная переустановка:

```bash
# Остановить и удалить всё
docker-compose down -v

# Удалить образы
docker rmi ch2-backend ch2-frontend

# Очистить кэш Docker
docker system prune -a

# Пересобрать с нуля
docker-compose up -d --build

# Применить миграции
docker exec chat_backend alembic upgrade head
```

## 🎨 Особенности:

### Hot Reload:
- ✅ Backend: Uvicorn автоматически перезагружается
- ✅ Frontend: Vite HMR работает
- ✅ Изменения применяются мгновенно

### Volumes:
- Код монтируется из хоста
- Изменения видны сразу
- node_modules изолированы

### Сеть:
- Все контейнеры в одной сети `ch2_default`
- Сервисы общаются по именам (postgres, backend, frontend)
- Порты проброшены на хост

## 🌐 Доступ к приложению:

1. Откройте браузер: http://localhost:3000
2. Создайте аккаунт или войдите
3. Тестируйте все функции!

## 📱 Тестирование:

- Desktop: http://localhost:3000
- Mobile: Откройте DevTools (F12) → Device Toolbar (Ctrl+Shift+M)
- API Docs: http://localhost:8000/docs

Готово! Проект работает в Docker! 🎉
