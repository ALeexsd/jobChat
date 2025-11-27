import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from datetime import date

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.core.database import Base

# Используем синхронное подключение
DATABASE_URL = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


def restore_users():
    """Восстановление базы пользователей (синхронная версия)"""
    
    # Создаем синхронный engine
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Создаем таблицы если их нет
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # Список пользователей для создания
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
                "role": UserRole.USER,
                "position": "Менеджер",
                "phone": "+79001234568"
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "user123",
                "first_name": "Мария",
                "last_name": "Петрова",
                "role": UserRole.USER,
                "position": "Разработчик",
                "phone": "+79001234569"
            },
            {
                "username": "user3",
                "email": "user3@example.com",
                "password": "user123",
                "first_name": "Алексей",
                "last_name": "Сидоров",
                "role": UserRole.USER,
                "position": "Дизайнер",
                "phone": "+79001234570"
            },
            {
                "username": "user4",
                "email": "user4@example.com",
                "password": "user123",
                "first_name": "Елена",
                "last_name": "Смирнова",
                "role": UserRole.USER,
                "position": "Аналитик",
                "phone": "+79001234571"
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        for user_data in users_data:
            # Проверка существования пользователя
            existing_user = session.query(User).filter(
                User.username == user_data["username"]
            ).first()
            
            if existing_user:
                print(f"⚠️  Пользователь {user_data['username']} уже существует, пропускаем")
                skipped_count += 1
                continue
            
            # Создание пользователя
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                birth_date=date(1990, 1, 1),
                role=user_data["role"],
                position=user_data.get("position"),
                phone=user_data.get("phone"),
                is_active=True,
                status="online"
            )
            
            session.add(user)
            created_count += 1
            print(f"✅ Создан пользователь: {user_data['username']} ({user_data['first_name']} {user_data['last_name']})")
        
        session.commit()
        
        print("\n" + "="*50)
        print(f"📊 Итого:")
        print(f"   Создано: {created_count}")
        print(f"   Пропущено: {skipped_count}")
        print("="*50)
        
        if created_count > 0:
            print("\n🔑 Данные для входа:")
            print("   Администратор:")
            print("     Username: admin")
            print("     Password: admin123")
            print("\n   Обычные пользователи:")
            print("     Username: user1, user2, user3, user4")
            print("     Password: user123")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("🔄 Восстановление базы пользователей...")
    print("="*50)
    restore_users()
