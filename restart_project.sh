#!/bin/bash

echo "========================================"
echo "Перезапуск проекта с очисткой кэша"
echo "========================================"
echo ""

# Останавливаем процессы (если запущены)
echo "[1/6] Останавливаем процессы..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "vite" 2>/dev/null
pkill -f "node.*vite" 2>/dev/null
sleep 2

# Очищаем кэш фронтенда
echo ""
echo "[2/6] Очищаем кэш фронтенда..."
cd frontend
rm -rf node_modules/.vite
rm -rf dist
rm -rf .vite
echo "Кэш фронтенда очищен!"

# Очищаем кэш Python
echo ""
echo "[3/6] Очищаем кэш Python..."
cd ../backend
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache
echo "Кэш Python очищен!"

# Запускаем бэкенд
echo ""
echo "[4/6] Запускаем бэкенд..."
cd ..
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Бэкенд запускается на http://localhost:8000 (PID: $BACKEND_PID)"
sleep 3

# Запускаем фронтенд
echo ""
echo "[5/6] Запускаем фронтенд..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Фронтенд запускается на http://localhost:5173 (PID: $FRONTEND_PID)"

echo ""
echo "[6/6] Готово!"
echo "========================================"
echo "Проект перезапущен с очисткой кэша"
echo "========================================"
echo ""
echo "Бэкенд:   http://localhost:8000 (PID: $BACKEND_PID)"
echo "Фронтенд: http://localhost:5173 (PID: $FRONTEND_PID)"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Для остановки используйте:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Ждем завершения
wait
