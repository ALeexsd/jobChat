# Production Deployment Guide

Руководство по развертыванию корпоративного мессенджера в production окружении.

## 📋 Требования

### Минимальные требования к серверу
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 20 GB SSD
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+

### Рекомендуемые требования
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 50+ GB SSD
- **OS**: Ubuntu 22.04 LTS

### Необходимое ПО
- Docker 20.10+
- Docker Compose 2.0+
- Nginx (для reverse proxy)
- Certbot (для SSL сертификатов)

## 🚀 Пошаговое развертывание

### 1. Подготовка сервера

#### Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

#### Установка Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Установка Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Установка Nginx
```bash
sudo apt install nginx -y
```

#### Установка Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Клонирование проекта

```bash
cd /opt
sudo git clone <repository-url> corporate-messenger
cd corporate-messenger
sudo chown -R $USER:$USER .
```

### 3. Настройка переменных окружения

#### Backend (.env)
```bash
cd backend
cp .env.example .env
nano .env
```

Обязательно измените:
```env
DATABASE_URL=postgresql://chatuser:STRONG_PASSWORD@postgres:5432/chatdb
SECRET_KEY=GENERATE_STRONG_SECRET_KEY_HERE
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_FILE_SIZE=10485760
```

Генерация SECRET_KEY:
```bash
openssl rand -hex 32
```

#### Frontend (.env)
```bash
cd ../frontend
cp .env.example .env
nano .env
```

Измените на ваш домен:
```env
VITE_API_URL=https://your-domain.com/api
VITE_WS_URL=wss://your-domain.com
```

### 4. Настройка Docker Compose для Production

Создайте `docker-compose.prod.yml`:

```yaml
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
      dockerfile: Dockerfile.prod
    container_name: chat_backend
    restart: always
    environment:
      DATABASE_URL: postgresql://chatuser:${POSTGRES_PASSWORD}@postgres:5432/chatdb
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - media_files:/app/media
    networks:
      - chat_network
    command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: chat_frontend
    restart: always
    networks:
      - chat_network

  nginx:
    image: nginx:alpine
    container_name: chat_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - media_files:/var/www/media:ro
    depends_on:
      - backend
      - frontend
    networks:
      - chat_network

volumes:
  postgres_data:
  media_files:

networks:
  chat_network:
    driver: bridge
```

### 5. Создание Production Dockerfile

#### Backend Dockerfile.prod
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

#### Frontend Dockerfile.prod
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 6. Настройка Nginx

Создайте `/opt/corporate-messenger/nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=ws_limit:10m rate=5r/s;

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 10M;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api {
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket
        location /ws {
            limit_req zone=ws_limit burst=10 nodelay;
            
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }

        # Media files
        location /media {
            alias /var/www/media;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # API Documentation
        location /docs {
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }
    }
}
```

### 7. Получение SSL сертификата

```bash
sudo certbot certonly --nginx -d your-domain.com
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem /opt/corporate-messenger/nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem /opt/corporate-messenger/nginx/ssl/
```

Автоматическое обновление:
```bash
sudo crontab -e
```

Добавьте:
```
0 0 * * 0 certbot renew --quiet && cp /etc/letsencrypt/live/your-domain.com/*.pem /opt/corporate-messenger/nginx/ssl/ && docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml restart nginx
```

### 8. Запуск приложения

```bash
cd /opt/corporate-messenger

# Создание .env файла с паролями
echo "POSTGRES_PASSWORD=$(openssl rand -hex 16)" > .env.prod
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env.prod

# Запуск
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Создание администратора
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_admin.py
```

### 9. Настройка автоматических бэкапов

Создайте скрипт `/opt/corporate-messenger/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/opt/corporate-messenger/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"

# Создание бэкапа
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

# Удаление старых бэкапов (старше 30 дней)
find ${BACKUP_DIR} -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup created: ${BACKUP_FILE}"
```

Сделайте скрипт исполняемым:
```bash
chmod +x /opt/corporate-messenger/backup.sh
```

Добавьте в crontab (ежедневно в 2:00):
```bash
sudo crontab -e
```

```
0 2 * * * /opt/corporate-messenger/backup.sh >> /var/log/chat-backup.log 2>&1
```

### 10. Мониторинг и логирование

#### Просмотр логов
```bash
# Все сервисы
docker-compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yml logs -f backend

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

#### Мониторинг ресурсов
```bash
docker stats
```

#### Настройка logrotate
Создайте `/etc/logrotate.d/docker-chat`:

```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
```

### 11. Firewall настройка

```bash
# UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### 12. Обновление приложения

```bash
cd /opt/corporate-messenger

# Остановка сервисов
docker-compose -f docker-compose.prod.yml down

# Обновление кода
git pull origin main

# Пересборка образов
docker-compose -f docker-compose.prod.yml build

# Запуск
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## 🔒 Безопасность

### Рекомендации по безопасности

1. **Используйте сильные пароли**
   - Для БД
   - Для SECRET_KEY
   - Для пользователей

2. **Регулярно обновляйте систему**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Настройте fail2ban**
   ```bash
   sudo apt install fail2ban -y
   sudo systemctl enable fail2ban
   ```

4. **Ограничьте доступ к БД**
   - БД должна быть доступна только из Docker сети

5. **Используйте HTTPS**
   - Всегда используйте SSL сертификаты

6. **Регулярные бэкапы**
   - Настройте автоматические бэкапы
   - Храните бэкапы в безопасном месте

## 📊 Мониторинг

### Установка Prometheus и Grafana (опционально)

```bash
# Добавьте в docker-compose.prod.yml

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - "9090:9090"
    networks:
      - chat_network

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - chat_network
```

## 🆘 Troubleshooting

### Проблема: Контейнеры не запускаются
```bash
# Проверка логов
docker-compose -f docker-compose.prod.yml logs

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

### Проблема: БД недоступна
```bash
# Проверка подключения
docker-compose -f docker-compose.prod.yml exec postgres psql -U chatuser -d chatdb

# Перезапуск БД
docker-compose -f docker-compose.prod.yml restart postgres
```

### Проблема: Высокая нагрузка
```bash
# Увеличьте количество workers в gunicorn
# В docker-compose.prod.yml измените:
command: gunicorn app.main:app -w 8 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи
2. Проверьте документацию
3. Создайте issue в GitHub

---

**Важно**: Перед развертыванием в production обязательно протестируйте все функции в staging окружении!
