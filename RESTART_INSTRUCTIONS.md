# 🔄 Инструкция по перезапуску проекта

## 🚀 Быстрый перезапуск с очисткой кэша

### Windows

Запустите файл:
```bash
restart_project.bat
```

Или вручную:
```bash
# 1. Остановите процессы
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# 2. Очистите кэш фронтенда
cd frontend
rmdir /s /q node_modules\.vite
rmdir /s /q dist
rmdir /s /q .vite

# 3. Очистите кэш Python
cd ..\backend
for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

# 4. Запустите бэкенд
cd ..
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# 5. Запустите фронтенд
start cmd /k "cd frontend && npm run dev"
```

### Linux/Mac

Запустите файл:
```bash
chmod +x restart_project.sh
./restart_project.sh
```

Или вручную:
```bash
# 1. Остановите процессы
pkill -f "uvicorn"
pkill -f "vite"

# 2. Очистите кэш фронтенда
cd frontend
rm -rf node_modules/.vite dist .vite

# 3. Очистите кэш Python
cd ../backend
find . -type d -name "__pycache__" -exec rm -rf {} +

# 4. Запустите бэкенд
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# 5. Запустите фронтенд
cd ../frontend
npm run dev &
```

## 🌐 URL адреса

После запуска проект будет доступен по адресам:

- **Фронтенд:** http://localhost:5173
- **Бэкенд:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs
- **WebSocket:** ws://localhost:8000/ws

## ✅ Проверка запуска

### 1. Проверьте бэкенд

Откройте в браузере: http://localhost:8000/health

Должен вернуть:
```json
{"status":"healthy"}
```

### 2. Проверьте фронтенд

Откройте в браузере: http://localhost:5173

Должна открыться страница входа.

### 3. Проверьте WebSocket

Откройте консоль браузера (F12) после входа в систему.

Должно быть сообщение:
```
✅ WebSocket connection established
```

## 🐛 Если что-то не работает

### Проблема: Порт занят

**Ошибка:** `Address already in use`

**Решение:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Проблема: Модули не найдены

**Ошибка:** `ModuleNotFoundError` или `Cannot find module`

**Решение:**
```bash
# Переустановите зависимости
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

### Проблема: База данных не подключается

**Ошибка:** `Connection refused` или `Database error`

**Решение:**
```bash
# Проверьте PostgreSQL
# Windows
sc query postgresql

# Linux/Mac
sudo systemctl status postgresql

# Запустите если не запущен
# Windows
net start postgresql

# Linux/Mac
sudo systemctl start postgresql
```

### Проблема: CORS ошибки

**Ошибка:** `CORS policy: No 'Access-Control-Allow-Origin'`

**Решение:**
1. Проверьте, что бэкенд запущен на порту 8000
2. Проверьте файл `frontend/.env`:
   ```
   VITE_API_URL=http://localhost:8000/api
   VITE_WS_URL=ws://localhost:8000
   ```
3. Перезапустите фронтенд

## 📝 Полезные команды

### Просмотр логов

**Бэкенд:**
```bash
cd backend
python -m uvicorn app.main:app --reload --log-level debug
```

**Фронтенд:**
```bash
cd frontend
npm run dev -- --debug
```

### Очистка всего кэша

```bash
# Windows
cd frontend
rmdir /s /q node_modules\.vite dist .vite
cd ..\backend
for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

# Linux/Mac
cd frontend
rm -rf node_modules/.vite dist .vite
cd ../backend
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Пересборка фронтенда

```bash
cd frontend
npm run build
```

### Проверка зависимостей

```bash
# Python
cd backend
pip list

# Node.js
cd frontend
npm list
```

## 🎯 После перезапуска

1. Откройте http://localhost:5173
2. Войдите в систему
3. Проверьте консоль (F12) на наличие ошибок
4. Проверьте WebSocket подключение
5. Протестируйте уведомления

## 📚 Дополнительная информация

- **BUGS_FIXED_NOTIFICATIONS.md** - исправленные баги
- **ROUTES_AND_TASKS_NOTIFICATIONS.md** - уведомления о задачах и маршрутах
- **CORS_FIX_ROUTES.md** - решение CORS проблем

## ✨ Готово!

Проект перезапущен с очисткой кэша. Все изменения применены! 🚀
