#!/bin/bash

# Скрипт автоматической установки корпоративного мессенджера на Ubuntu VPS
# Использование: sudo bash deploy-ubuntu.sh

set -e

echo "================================================"
echo "  Установка корпоративного мессенджера"
echo "  Ubuntu VPS Deployment Script"
echo "================================================"
echo ""

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Запустите скрипт с правами root: sudo bash deploy-ubuntu.sh"
    exit 1
fi

# Переменные
INSTALL_DIR="/opt/corporate-messenger"
DOMAIN=""
EMAIL=""

# Запрос домена
read -p "Введите ваш домен (например, chat.example.com): " DOMAIN
if [ -z "$DOMAIN" ]; then
    echo "❌ Домен обязателен!"
    exit 1
fi

# Запрос email для SSL
read -p "Введите email для SSL сертификата: " EMAIL
if [ -z "$EMAIL" ]; then
    echo "❌ Email обязателен!"
    exit 1
fi

echo ""
echo "📋 Параметры установки:"
echo "   Домен: $DOMAIN"
echo "   Email: $EMAIL"
echo "   Директория: $INSTALL_DIR"
echo ""
read -p "Продолжить? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo ""
echo "🔄 Шаг 1/10: Обновление системы..."
apt update && apt upgrade -y

echo ""
echo "🔄 Шаг 2/10: Установка необходимых пакетов..."
apt install -y curl git ufw fail2ban

echo ""
echo "🔄 Шаг 3/10: Установка Docker..."
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
echo "🔄 Шаг 4/10: Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

echo ""
echo "🔄 Шаг 5/10: Установка Nginx..."
apt install -y nginx
systemctl enable nginx
systemctl start nginx

echo ""
echo "🔄 Шаг 6/10: Установка Certbot для SSL..."
apt install -y certbot python3-certbot-nginx

echo ""
echo "🔄 Шаг 7/10: Настройка Firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw reload

echo ""
echo "🔄 Шаг 8/10: Копирование проекта..."
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  Директория $INSTALL_DIR уже существует"
    read -p "Удалить и создать заново? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
    else
        echo "❌ Установка прервана"
        exit 1
    fi
fi

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"
cd "$INSTALL_DIR"

echo ""
echo "🔄 Шаг 9/10: Генерация конфигурации..."

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
CORS_ORIGINS=https://${DOMAIN}
EOF

# Создание .env для frontend
cat > frontend/.env << EOF
VITE_API_URL=https://${DOMAIN}/api
VITE_WS_URL=wss://${DOMAIN}
EOF

# Создание docker-compose.prod.yml
cat > docker-compose.prod.yml << 'EOFCOMPOSE'
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
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - chat_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U chatuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chat_backend
    restart: always
    env_file:
      - ./backend/.env
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - media_files:/app/media
    networks:
      - chat_network
    ports:
      - "127.0.0.1:8000:8000"

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
      - "127.0.0.1:3000:80"

volumes:
  postgres_data:
  media_files:

networks:
  chat_network:
    driver: bridge
EOFCOMPOSE

# Добавление переменной в docker-compose
echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" > .env.prod

# Создание Nginx конфигурации
cat > /etc/nginx/sites-available/chat << EOFNGINX
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

# Rate limiting
limit_req_zone \$binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=ws_limit:10m rate=5r/s;

server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 10M;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API
    location /api {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # WebSocket
    location /ws {
        limit_req zone=ws_limit burst=10 nodelay;
        
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }

    # API Documentation
    location /docs {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
    }

    location /redoc {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
    }
}
EOFNGINX

ln -sf /etc/nginx/sites-available/chat /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t

echo ""
echo "🔄 Шаг 10/10: Получение SSL сертификата..."
certbot certonly --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL"

# Перезапуск Nginx
systemctl reload nginx

echo ""
echo "🚀 Запуск приложения..."
cd "$INSTALL_DIR"
docker-compose -f docker-compose.prod.yml up -d --build

echo ""
echo "⏳ Ожидание запуска сервисов (30 секунд)..."
sleep 30

echo ""
echo "🔄 Применение миграций базы данных..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

echo ""
echo "👤 Создание администратора..."
docker-compose -f docker-compose.prod.yml exec -T backend python -c "
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    username='admin',
    email='admin@example.com',
    full_name='Administrator',
    hashed_password=get_password_hash('admin123'),
    role='admin',
    is_active=True
)
db.add(admin)
db.commit()
print('✅ Администратор создан')
"

# Создание скрипта бэкапа
cat > "$INSTALL_DIR/backup.sh" << 'EOFBACKUP'
#!/bin/bash
BACKUP_DIR="/opt/corporate-messenger/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"

mkdir -p "$BACKUP_DIR"

docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

find ${BACKUP_DIR} -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup created: ${BACKUP_FILE}"
EOFBACKUP

chmod +x "$INSTALL_DIR/backup.sh"

# Добавление в crontab
(crontab -l 2>/dev/null; echo "0 2 * * * $INSTALL_DIR/backup.sh >> /var/log/chat-backup.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 0 * * 0 certbot renew --quiet && systemctl reload nginx") | crontab -

echo ""
echo "================================================"
echo "  ✅ Установка завершена успешно!"
echo "================================================"
echo ""
echo "📋 Информация для доступа:"
echo ""
echo "   🌐 URL: https://$DOMAIN"
echo "   👤 Логин: admin"
echo "   🔑 Пароль: admin123"
echo ""
echo "   📚 API Docs: https://$DOMAIN/docs"
echo "   📖 ReDoc: https://$DOMAIN/redoc"
echo ""
echo "⚠️  ВАЖНО: Смените пароль администратора после первого входа!"
echo ""
echo "📁 Файлы конфигурации:"
echo "   Проект: $INSTALL_DIR"
echo "   Backend .env: $INSTALL_DIR/backend/.env"
echo "   Frontend .env: $INSTALL_DIR/frontend/.env"
echo "   Nginx: /etc/nginx/sites-available/chat"
echo ""
echo "🔧 Полезные команды:"
echo "   Логи: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml logs -f"
echo "   Статус: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml ps"
echo "   Перезапуск: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml restart"
echo "   Остановка: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml down"
echo "   Бэкап: $INSTALL_DIR/backup.sh"
echo ""
echo "================================================"
