#!/bin/bash

echo "=================================="
echo "  Восстановление пользователей"
echo "=================================="
echo ""

# Создаем временный Python скрипт
cat > /tmp/create_users.py << 'EOF'
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import date
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole

async def create_users():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        from sqlalchemy import select
        
        users_data = [
            ("admin", "admin@example.com", "admin123", "Администратор", "Системы", UserRole.ADMIN, "Системный администратор", "+79001234567"),
            ("user1", "user1@example.com", "user123", "Иван", "Иванов", UserRole.USER, "Менеджер", "+79001234568"),
            ("user2", "user2@example.com", "user123", "Мария", "Петрова", UserRole.USER, "Разработчик", "+79001234569"),
            ("user3", "user3@example.com", "user123", "Алексей", "Сидоров", UserRole.USER, "Дизайнер", "+79001234570"),
            ("user4", "user4@example.com", "user123", "Елена", "Смирнова", UserRole.USER, "Аналитик", "+79001234571"),
        ]
        
        created = 0
        skipped = 0
        
        for username, email, password, first, last, role, position, phone in users_data:
            result = await session.execute(select(User).where(User.username == username))
            if result.scalar_one_or_none():
                print(f"⚠️  {username} - уже существует")
                skipped += 1
                continue
            
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
                first_name=first,
                last_name=last,
                birth_date=date(1990, 1, 1),
                role=role,
                position=position,
                phone=phone,
                is_active=True,
                status="online"
            )
            session.add(user)
            created += 1
            icon = "👑" if role == UserRole.ADMIN else "👤"
            print(f"✅ {icon} {username} - {first} {last}")
        
        await session.commit()
        
        print(f"\n📊 Создано: {created}, Пропущено: {skipped}")
        
        if created > 0:
            print("\n🔑 Данные для входа:")
            print("   👑 admin / admin123")
            print("   👤 user1-4 / user123")

asyncio.run(create_users())
EOF

# Копируем скрипт в контейнер и выполняем
echo "📋 Создание пользователей..."
docker cp /tmp/create_users.py chat_backend:/app/create_users.py
docker exec chat_backend python create_users.py

# Удаляем временный файл
rm /tmp/create_users.py

echo ""
echo "✅ Готово!"
echo "=================================="
