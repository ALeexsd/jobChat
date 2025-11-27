# Восстановление базы данных пользователей

## 🚨 Проблема
База данных пользователей слетела или пуста.

## ✅ Решение

### Вариант 1: Через Docker (Рекомендуется)

#### Шаг 1: Проверьте, что Docker контейнеры запущены
```bash
docker-compose ps
```

Должны быть запущены:
- postgres
- backend
- frontend

#### Шаг 2: Подключитесь к контейнеру backend
```bash
docker-compose exec backend bash
```

#### Шаг 3: Запустите скрипт создания администратора
```bash
python scripts/create_admin.py
```

Или создайте пользователей через Python:
```bash
python
```

Затем выполните:
```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import date
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole

DATABASE_URL = settings.DATABASE_URL

async def create_users():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Администратор
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Администратор",
            last_name="Системы",
            birth_date=date(1990, 1, 1),
            role=UserRole.ADMIN,
            position="Системный администратор",
            phone="+79001234567",
            is_active=True,
            status="online"
        )
        session.add(admin)
        
        # Пользователи
        users_data = [
            ("user1", "Иван", "Иванов", "Менеджер"),
            ("user2", "Мария", "Петрова", "Разработчик"),
            ("user3", "Алексей", "Сидоров", "Дизайнер"),
            ("user4", "Елена", "Смирнова", "Аналитик"),
        ]
        
        for i, (username, first, last, position) in enumerate(users_data, 1):
            user = User(
                username=username,
                email=f"{username}@example.com",
                hashed_password=get_password_hash("user123"),
                first_name=first,
                last_name=last,
                birth_date=date(1990, 1, 1),
                role=UserRole.USER,
                position=position,
                phone=f"+7900123456{7+i}",
                is_active=True,
                status="online"
            )
            session.add(user)
        
        await session.commit()
        print("✅ Пользователи созданы!")

asyncio.run(create_users())
```

Нажмите Ctrl+D для выхода из Python.

---

### Вариант 2: Через SQL напрямую

#### Шаг 1: Подключитесь к PostgreSQL
```bash
docker-compose exec postgres psql -U chatuser -d chatdb
```

#### Шаг 2: Проверьте таблицу users
```sql
SELECT id, username, email, first_name, last_name, role FROM users;
```

#### Шаг 3: Если таблица пуста, создайте пользователей через SQL
```sql
-- Администратор (пароль: admin123)
INSERT INTO users (username, email, hashed_password, first_name, last_name, birth_date, role, position, phone, is_active, status)
VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3rG',
    'Администратор',
    'Системы',
    '1990-01-01',
    'admin',
    'Системный администратор',
    '+79001234567',
    true,
    'online'
);

-- Пользователь 1 (пароль: user123)
INSERT INTO users (username, email, hashed_password, first_name, last_name, birth_date, role, position, phone, is_active, status)
VALUES (
    'user1',
    'user1@example.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'Иван',
    'Иванов',
    '1990-01-01',
    'user',
    'Менеджер',
    '+79001234568',
    true,
    'online'
);

-- Добавьте остальных пользователей аналогично
```

Выйдите: `\q`

---

### Вариант 3: Пересоздание базы данных

#### Шаг 1: Остановите контейнеры
```bash
docker-compose down
```

#### Шаг 2: Удалите volume с базой данных
```bash
docker volume rm ch2_postgres_data
```

#### Шаг 3: Запустите контейнеры заново
```bash
docker-compose up -d
```

#### Шаг 4: Примените миграции
```bash
docker-compose exec backend alembic upgrade head
```

#### Шаг 5: Создайте пользователей (см. Вариант 1)

---

### Вариант 4: Через API (если backend работает)

Создайте файл `create_users.sh`:

```bash
#!/bin/bash

# Регистрация администратора
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "first_name": "Администратор",
    "last_name": "Системы",
    "birth_date": "1990-01-01"
  }'

# Регистрация пользователей
for i in {1..4}; do
  curl -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"user$i\",
      \"email\": \"user$i@example.com\",
      \"password\": \"user123\",
      \"first_name\": \"User\",
      \"last_name\": \"$i\",
      \"birth_date\": \"1990-01-01\"
    }"
done
```

Запустите:
```bash
chmod +x create_users.sh
./create_users.sh
```

**Примечание:** Затем нужно вручную изменить роль администратора в базе:
```sql
UPDATE users SET role = 'admin' WHERE username = 'admin';
```

---

## 🔑 Данные для входа

После восстановления используйте:

### Администратор
- **Username:** admin
- **Password:** admin123

### Обычные пользователи
- **Username:** user1, user2, user3, user4
- **Password:** user123

---

## 🧪 Проверка

### Через API
```bash
# Получить токен
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Проверить пользователей
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Через интерфейс
1. Откройте http://localhost:5173
2. Войдите как admin / admin123
3. Проверьте список пользователей

---

## 📝 Хеши паролей

Если нужно создать пользователей через SQL, используйте эти хеши:

- **admin123:** `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3rG`
- **user123:** `$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW`

---

## 🐛 Решение проблем

### Ошибка: "ModuleNotFoundError: No module named 'asyncpg'"
**Решение:** Используйте Docker (Вариант 1) или SQL (Вариант 2)

### Ошибка: "relation 'users' does not exist"
**Решение:** Примените миграции:
```bash
docker-compose exec backend alembic upgrade head
```

### Ошибка: "duplicate key value violates unique constraint"
**Решение:** Пользователь уже существует. Проверьте:
```sql
SELECT * FROM users WHERE username = 'admin';
```

### База данных пуста после перезапуска
**Решение:** Проверьте, что volume сохраняется:
```bash
docker volume ls | grep postgres
```

---

## 💡 Быстрое решение (Рекомендуется)

Самый простой способ:

```bash
# 1. Войдите в контейнер
docker-compose exec backend bash

# 2. Запустите Python
python

# 3. Скопируйте и вставьте весь код из Варианта 1, Шаг 3

# 4. Выйдите
exit
exit

# 5. Проверьте
# Откройте http://localhost:5173 и войдите как admin/admin123
```

---

## ✅ Готово!

После выполнения любого из вариантов вы сможете войти в систему.

Если проблемы остались, проверьте логи:
```bash
docker-compose logs backend
docker-compose logs postgres
```
