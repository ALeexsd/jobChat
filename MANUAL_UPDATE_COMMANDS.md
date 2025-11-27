# Команды для ручного обновления проекта

## 🔄 Обновление Docker контейнеров

### Перезапуск всех контейнеров
```bash
docker restart chat_frontend chat_backend chat_postgres
```

### Перезапуск отдельных контейнеров
```bash
# Только фронтенд
docker restart chat_frontend

# Только бэкенд
docker restart chat_backend

# Только база данных
docker restart chat_postgres
```

### Остановка и запуск контейнеров
```bash
# Остановить все
docker stop chat_frontend chat_backend chat_postgres

# Запустить все
docker start chat_postgres chat_backend chat_frontend
```

### Пересборка контейнеров (если изменились Dockerfile или зависимости)
```bash
# Остановить и удалить контейнеры
docker stop chat_frontend chat_backend
docker rm chat_frontend chat_backend

# Пересобрать и запустить
docker-compose up -d --build
```

## 📦 Обновление зависимостей

### Frontend (Node.js)
```bash
# Войти в контейнер
docker exec -it chat_frontend sh

# Установить новые зависимости
npm install

# Выйти
exit

# Перезапустить контейнер
docker restart chat_frontend
```

### Backend (Python)
```bash
# Войти в контейнер
docker exec -it chat_backend sh

# Установить новые зависимости
pip install -r requirements.txt

# Выйти
exit

# Перезапустить контейнер
docker restart chat_backend
```

## 🗄️ Работа с базой данных

### Подключение к PostgreSQL
```bash
docker exec -it chat_postgres psql -U chatuser -d chatdb
```

### Выполнение SQL команд
```bash
# Просмотр пользователей
docker exec chat_postgres psql -U chatuser -d chatdb -c "SELECT id, username, role FROM users;"

# Изменение роли пользователя
docker exec chat_postgres psql -U chatuser -d chatdb -c "UPDATE users SET role = 'ADMIN' WHERE username = 'username';"

# Сброс пароля (хеш для пароля "password123")
docker exec chat_postgres psql -U chatuser -d chatdb -c "UPDATE users SET hashed_password = '\$2b\$12\$...' WHERE username = 'username';"
```

### Резервное копирование базы данных
```bash
# Создать бэкап
docker exec chat_postgres pg_dump -U chatuser chatdb > backup.sql

# Восстановить из бэкапа
docker exec -i chat_postgres psql -U chatuser chatdb < backup.sql
```

## 📝 Просмотр логов

### Логи контейнеров
```bash
# Последние 50 строк логов фронтенда
docker logs chat_frontend --tail 50

# Последние 50 строк логов бэкенда
docker logs chat_backend --tail 50

# Следить за логами в реальном времени
docker logs -f chat_backend
```

### Логи с фильтрацией
```bash
# Только ошибки
docker logs chat_backend 2>&1 | Select-String "ERROR"

# Только определенный endpoint
docker logs chat_backend 2>&1 | Select-String "/api/tasks"
```

## 🔍 Проверка статуса

### Статус контейнеров
```bash
# Все контейнеры
docker ps -a

# Только запущенные
docker ps

# С использованием ресурсов
docker stats
```

### Проверка сети
```bash
# Проверить доступность фронтенда
curl http://localhost:3000

# Проверить доступность бэкенда
curl http://localhost:8000/docs

# Проверить API
curl http://localhost:8000/api/users/
```

## 🧹 Очистка

### Удаление неиспользуемых ресурсов
```bash
# Удалить остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune

# Удалить все неиспользуемые ресурсы
docker system prune -a
```

### Полная очистка и пересборка
```bash
# Остановить все контейнеры
docker-compose down

# Удалить volumes (ВНИМАНИЕ: удалит данные БД!)
docker-compose down -v

# Пересобрать и запустить
docker-compose up -d --build
```

## 🔧 Отладка

### Войти в контейнер
```bash
# Frontend
docker exec -it chat_frontend sh

# Backend
docker exec -it chat_backend sh

# PostgreSQL
docker exec -it chat_postgres sh
```

### Проверить переменные окружения
```bash
docker exec chat_backend env
docker exec chat_frontend env
```

### Проверить файлы в контейнере
```bash
# Список файлов фронтенда
docker exec chat_frontend ls -la /app/src

# Список файлов бэкенда
docker exec chat_backend ls -la /app
```

## 🚀 Быстрые команды

### Полный перезапуск проекта
```bash
docker restart chat_postgres chat_backend chat_frontend
```

### Проверка здоровья
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Просмотр использования ресурсов
```bash
docker stats --no-stream
```

## 📌 Текущая конфигурация

**Контейнеры:**
- `chat_postgres` - PostgreSQL (порт 5432)
- `chat_backend` - FastAPI (порт 8000)
- `chat_frontend` - Vue.js + Vite (порт 3000)

**Учетные данные БД:**
- User: `chatuser`
- Password: `chatpass`
- Database: `chatdb`

**Доступ:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

---

✅ **Контейнеры обновлены и запущены!**
