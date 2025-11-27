"""
Восстановление пользователей с правильным драйвером
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import date
import sys
import os

sys.path.insert(0, '/app')

from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Правильный URL с asyncpg
DATABASE_URL = "postgresql+asyncpg://chatuser:chatpass@postgres:5432/chatdb"

async def create_users():
    print("\n" + "="*50)
    print("  🔄 ВОССТАНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ")
    print("="*50 + "\n")
    
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            from sqlalchemy import select
            
            users_data = [
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    "password": "admin123",
                    "first_name": "Администратор",
                    "last_name": "Системы",
                    "role": UserRole.ADMIN,
                    "position": "Системный администратор",
                    "phone": "+79001234567"
                },
                {
                    "username": "user1",
                    "email": "user1@example.com",
                    "password": "user123",
                    "first_name": "Иван",
                    "last_name": "Иванов",
                    "role": UserRole.EMPLOYEE,
                    "position": "Менеджер",
                    "phone": "+79001234568"
                },
                {
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "user123",
                    "first_name": "Мария",
                    "last_name": "Петрова",
                    "role": UserRole.EMPLOYEE,
                    "position": "Разработчик",
                    "phone": "+79001234569"
                },
                {
                    "username": "user3",
                    "email": "user3@example.com",
                    "password": "user123",
                    "first_name": "Алексей",
                    "last_name": "Сидоров",
                    "role": UserRole.EMPLOYEE,
                    "position": "Дизайнер",
                    "phone": "+79001234570"
                },
                {
                    "username": "user4",
                    "email": "user4@example.com",
                    "password": "user123",
                    "first_name": "Елена",
                    "last_name": "Смирнова",
                    "role": UserRole.EMPLOYEE,
                    "position": "Аналитик",
                    "phone": "+79001234571"
                }
            ]
            
            created = 0
            skipped = 0
            
            print("👥 Создание пользователей...")
            print("-" * 50)
            
            for user_data in users_data:
                result = await session.execute(
                    select(User).where(User.username == user_data["username"])
                )
                existing = result.scalar_one_or_none()
                
                if existing:
                    print(f"⚠️  {user_data['username']:10} - уже существует")
                    skipped += 1
                    continue
                
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    birth_date=date(1990, 1, 1),
                    role=user_data["role"],
                    position=user_data["position"],
                    phone=user_data["phone"],
                    is_active=True,
                    status="online"
                )
                
                session.add(user)
                created += 1
                
                icon = "👑" if user_data["role"] == UserRole.ADMIN else "👤"
                print(f"✅ {icon} {user_data['username']:10} - {user_data['first_name']} {user_data['last_name']}")
            
            await session.commit()
            
            print("-" * 50)
            print(f"\n📊 Результат:")
            print(f"   ✅ Создано:   {created}")
            print(f"   ⚠️  Пропущено: {skipped}")
            print("=" * 50)
            
            if created > 0:
                print("\n🔑 Данные для входа:")
                print("\n   👑 Администратор:")
                print("      Username: admin")
                print("      Password: admin123")
                print("\n   👤 Обычные пользователи:")
                print("      Username: user1, user2, user3, user4")
                print("      Password: user123")
                print("\n✨ Готово! Можете входить в систему.")
            else:
                print("\n✨ Все пользователи уже существуют!")
            
            print("\n" + "=" * 50 + "\n")
            
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(create_users())
