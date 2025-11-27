#!/bin/bash

# Упрощенная установка для серверов с малой памятью (1GB RAM)
# Использование: bash install-low-memory.sh

set -e

echo "================================================"
echo "  Установка корпоративного мессенджера"
echo "  Режим: Низкая память (1GB RAM)"
echo "================================================"
echo ""

DOMAIN="3x.tw1.ru"
EMAIL="admin@3x.tw1.ru"
INSTALL_DIR="/opt/corporate-messenger"

echo "📋 Параметры:"
echo "   Домен: $DOMAIN"
echo "   Директория: $INSTALL_DIR"
echo ""

# Шаг 1: Создание SWAP (критически важно для 1GB RAM!)
echo "🔄 Шаг 1/8: Создание SWAP файла (2GB)..."
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "✅ SWAP создан"
else
    echo "✅ SWAP уже существует"
fi

free -h

echo ""
echo "🔄 Шаг 2/8: Обновление системы..."
apt update

echo ""
echo "🔄 Шаг 3/8: Установка необходимых пакетов..."
apt install -y curl git ufw

echo ""
echo "🔄 Шаг 4/8: Установка Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker установлен"
else
    echo "✅ Docker уже установлен"
fi

echo ""
echo "🔄 Шаг 5/8: Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

echo ""
echo "🔄 Шаг 6/8: Настройка Firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw allow 3000/tcp
ufw reload

echo ""
echo "🔄 Шаг 7/8: Подготовка директории проекта..."
mkdir -p "$INSTALL_DIR"

# Проверяем, есть ли уже файлы проекта
if [ ! -f "$INSTALL_DIR/docker-compose.yml" ]; then
    echo "⚠️  Файлы проекта не найдены в $INSTALL_DIR"
    echo ""
    echo "Необходимо загрузить файлы проекта!"
    echo ""
    echo "Выполните на вашем компьютере:"
    echo "  1. Создайте архив: tar -czf project.tar.gz *"
    echo "  2. Загрузите: scp project.tar.gz root@2a03:6f00:a::1:55eb:/tmp/"
    echo "  3. На VPS: tar -xzf /tmp/project.tar.gz -C $INSTALL_DIR"
    echo ""
    echo "Или клонируйте из Git:"
    echo "  cd $INSTALL_DIR"
    echo "  git clone <repository-url> ."
    echo ""
    exit 1
fi

cd "$INSTALL_DIR"

echo ""
echo "🔄 Шаг 8/8: Генерация конфигурации..."

# Генерация паролей
POSTGRES_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)

# Создание .env для backend
cat > backend/.env << EOF
DATABASE_URL=postgresql://chatuser:${POSTGRES_PASSWORD}@postgres:5432/chatdb
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_FILE_SIZE=10485760
CORS_ORIGINS=http://${DOMAIN},http://localhost:3000
EOF

# Создание .env для frontend
cat > frontend/.env << EOF
VITE_API_URL=http://${DOMAIN}:8000/api
VITE_WS_URL=ws://${DOMAIN}:8000
EOF

# Создание docker-compose для низкой памяти
cat > docker-compose.low-memory.yml << 'EOFCOMPOSE'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: chat_postgres
    restart: always
    environment:
      POSTGRES_USER: chatuser
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: chatdb
      # Оптимизация для малой памяти
      POSTGRES_SHARED_BUFFERS: 128MB
      POSTGRES_EFFECTIVE_CACHE_SIZE: 256MB
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - chat_network
    command: postgres -c shared_buffers=128MB -c effective_cache_size=256MB -c max_connections=20
    deploy:
      resources:
        limits:
          memory: 256M

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chat_backend
    restart: always
    env_file:
      - ./backend/.env
    depends_on:
      - postgres
    volumes:
      - media_files:/app/media
    networks:
      - chat_network
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 384M

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: chat_frontend
    restart: always
    env_file:
      - ./frontend/.env
    networks:
      - chat_network
    ports:
      - "3000:80"
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  postgres_data:
  media_files:

networks:
  chat_network:
    driver: bridge
EOFCOMPOSE

echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" > .env.prod

echo ""
echo "✅ Конфигурация создана!"
echo ""
echo "================================================"
echo "  Готово к запуску!"
echo "================================================"
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. Убедитесь что файлы проекта в $INSTALL_DIR"
echo ""
echo "2. Запустите приложение:"
echo "   cd $INSTALL_DIR"
echo "   docker-compose -f docker-compose.low-memory.yml up -d --build"
echo ""
echo "3. Примените миграции:"
echo "   docker-compose -f docker-compose.low-memory.yml exec backend alembic upgrade head"
echo ""
echo "4. Создайте администратора:"
echo "   docker-compose -f docker-compose.low-memory.yml exec backend python -c \""
echo "from app.core.database import SessionLocal"
echo "from app.models.user import User"
echo "from app.core.security import get_password_hash"
echo "db = SessionLocal()"
echo "admin = User(username='admin', email='admin@example.com', full_name='Administrator', hashed_password=get_password_hash('admin123'), role='admin', is_active=True)"
echo "db.add(admin)"
echo "db.commit()"
echo "\""
echo ""
echo "5. Откройте в браузере:"
echo "   http://$DOMAIN:8000/docs (API)"
echo "   http://$DOMAIN:3000 (Frontend)"
echo ""
echo "⚠️  ВАЖНО: Из-за малого объема RAM (1GB) приложение может работать медленно!"
echo "   Рекомендуется увеличить RAM до 4GB для нормальной работы."
echo ""
echo "================================================"
