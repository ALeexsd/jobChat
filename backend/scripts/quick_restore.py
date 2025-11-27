"""
Быстрое восстановление пользователей
Независимый скрипт без импорта app модулей
"""
import sys
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date
from passlib.context import CryptContext
import enum

# Настройки
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/messenger_db"

# Создаем Base
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Enum для ролей
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


# Модель User (упрощенная)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    position = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="online")
    avatar_url = Column(String, nullable=True)


def restore_users():
    """Восстановление базы пользователей"""
    
    print("🔄 Подключение к базе данных...")
    engine = create_engine(DATABASE_URL, echo=False)
    
    print("📋 Создание таблиц (если нужно)...")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # Список пользователей
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
            },
            {
                "username": "user5",
                "email": "user5@example.com",
                "password": "user123",
                "first_name": "Дмитрий",
                "last_name": "Козлов",
                "role": UserRole.USER,
                "position": "Тестировщик",
                "phone": "+79001234572"
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        print("\n👥 Создание пользователей...")
        print("="*50)
        
        for user_data in users_data:
            # Проверка существования
            existing = session.query(User).filter(
                User.username == user_data["username"]
            ).first()
            
            if existing:
                print(f"⚠️  {user_data['username']:10} - уже существует")
                skipped_count += 1
                continue
            
            # Создание
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
            
            role_icon = "👑" if user_data["role"] == UserRole.ADMIN else "👤"
            print(f"✅ {role_icon} {user_data['username']:10} - {user_data['first_name']} {user_data['last_name']}")
        
        session.commit()
        
        print("="*50)
        print(f"\n📊 Результат:")
        print(f"   ✅ Создано:   {created_count}")
        print(f"   ⚠️  Пропущено: {skipped_count}")
        print("="*50)
        
        if created_count > 0:
            print("\n🔑 Данные для входа:")
            print("\n   👑 Администратор:")
            print("      Username: admin")
            print("      Password: admin123")
            print("\n   👤 Обычные пользователи:")
            print("      Username: user1, user2, user3, user4, user5")
            print("      Password: user123")
            print("\n✨ Готово! Можете входить в систему.")
        else:
            print("\n✨ Все пользователи уже существуют!")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        session.rollback()
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🔄 ВОССТАНОВЛЕНИЕ БАЗЫ ПОЛЬЗОВАТЕЛЕЙ")
    print("="*50 + "\n")
    restore_users()
    print("\n" + "="*50 + "\n")
