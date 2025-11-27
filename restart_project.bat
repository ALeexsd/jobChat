@echo off
echo ========================================
echo Перезапуск проекта с очисткой кэша
echo ========================================
echo.

REM Останавливаем процессы (если запущены)
echo [1/6] Останавливаем процессы...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Очищаем кэш фронтенда
echo.
echo [2/6] Очищаем кэш фронтенда...
cd frontend
if exist node_modules\.vite rmdir /s /q node_modules\.vite
if exist dist rmdir /s /q dist
if exist .vite rmdir /s /q .vite
echo Кэш фронтенда очищен!

REM Очищаем кэш Python
echo.
echo [3/6] Очищаем кэш Python...
cd ..\backend
if exist __pycache__ rmdir /s /q __pycache__
for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
if exist .pytest_cache rmdir /s /q .pytest_cache
echo Кэш Python очищен!

REM Запускаем бэкенд
echo.
echo [4/6] Запускаем бэкенд...
cd ..
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo Бэкенд запускается на http://localhost:8000
timeout /t 3 /nobreak >nul

REM Запускаем фронтенд
echo.
echo [5/6] Запускаем фронтенд...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
echo Фронтенд запускается на http://localhost:5173

echo.
echo [6/6] Готово!
echo ========================================
echo Проект перезапущен с очисткой кэша
echo ========================================
echo.
echo Бэкенд:  http://localhost:8000
echo Фронтенд: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Нажмите любую клавишу для выхода...
pause >nul
