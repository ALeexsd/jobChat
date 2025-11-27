import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole

DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


async def create_admin_user():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Проверка существования админа
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "admin"))
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Admin user already exists!")
            return

        # Создание админа
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=UserRole.ADMIN,
            is_active=True
        )

        session.add(admin)
        await session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin_user())
