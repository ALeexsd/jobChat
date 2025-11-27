@echo off
echo ==================================
echo   Восстановление пользователей
echo ==================================
echo.

REM Создаем временный Python скрипт
(
echo import asyncio
echo from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
echo from sqlalchemy.orm import sessionmaker
echo from datetime import date
echo from app.core.config import settings
echo from app.core.security import get_password_hash
echo from app.models.user import User, UserRole
echo.
echo async def create_users^(^):
echo     engine = create_async_engine^(settings.DATABASE_URL, echo=False^)
echo     async_session = sessionmaker^(engine, class_=AsyncSession, expire_on_commit=False^)
echo     async with async_session^(^) as session:
echo         from sqlalchemy import select
echo         users_data = [
echo             ^("admin", "admin@example.com", "admin123", "Администратор", "Системы", UserRole.ADMIN, "Системный администратор", "+79001234567"^),
echo             ^("user1", "user1@example.com", "user123", "Иван", "Иванов", UserRole.USER, "Менеджер", "+79001234568"^),
echo             ^("user2", "user2@example.com", "user123", "Мария", "Петрова", UserRole.USER, "Разработчик", "+79001234569"^),
echo             ^("user3", "user3@example.com", "user123", "Алексей", "Сидоров", UserRole.USER, "Дизайнер", "+79001234570"^),
echo             ^("user4", "user4@example.com", "user123", "Елена", "Смирнова", UserRole.USER, "Аналитик", "+79001234571"^),
echo         ]
echo         created = 0
echo         skipped = 0
echo         for username, email, password, first, last, role, position, phone in users_data:
echo             result = await session.execute^(select^(User^).where^(User.username == username^)^)
echo             if result.scalar_one_or_none^(^):
echo                 print^(f"⚠️  {username} - уже существует"^)
echo                 skipped += 1
echo                 continue
echo             user = User^(
echo                 username=username, email=email,
echo                 hashed_password=get_password_hash^(password^),
echo                 first_name=first, last_name=last,
echo                 birth_date=date^(1990, 1, 1^), role=role,
echo                 position=position, phone=phone,
echo                 is_active=True, status="online"
echo             ^)
echo             session.add^(user^)
echo             created += 1
echo             icon = "👑" if role == UserRole.ADMIN else "👤"
echo             print^(f"✅ {icon} {username} - {first} {last}"^)
echo         await session.commit^(^)
echo         print^(f"\n📊 Создано: {created}, Пропущено: {skipped}"^)
echo         if created ^> 0:
echo             print^("\n🔑 Данные для входа:"^)
echo             print^("   👑 admin / admin123"^)
echo             print^("   👤 user1-4 / user123"^)
echo.
echo asyncio.run^(create_users^(^)^)
) > create_users_temp.py

echo 📋 Создание пользователей...
docker cp create_users_temp.py chat_backend:/app/create_users.py
docker exec chat_backend python create_users.py

REM Удаляем временный файл
del create_users_temp.py

echo.
echo ✅ Готово!
echo ==================================
pause
