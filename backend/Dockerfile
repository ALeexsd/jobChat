FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    sqlalchemy==2.0.23 \
    alembic==1.12.1 \
    asyncpg==0.29.0 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    email-validator==2.1.0 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    bcrypt==4.0.1 \
    python-multipart==0.0.6 \
    websockets==12.0 \
    aiofiles==23.2.1 \
    pillow==10.1.0

# Копирование кода
COPY . .

# Создание директории для медиа
RUN mkdir -p /app/media

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
