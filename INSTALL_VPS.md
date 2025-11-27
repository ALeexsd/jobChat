# 🚀 Установка на VPS Ubuntu

Полное руководство по развертыванию корпоративного мессенджера на VPS с Ubuntu.

## 📋 Требования

### Минимальные требования к серверу
- **OS**: Ubuntu 20.04 / 22.04 LTS
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 20 GB SSD
- **Домен**: Настроенный A-запись на IP сервера

### Рекомендуемые требования
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 50+ GB SSD

## 🎯 Быстрая установка (Автоматическая)

### Шаг 1: Подключитесь к серверу
```bash
ssh root@your-server-ip
```

### Шаг 2: Скачайте проект
```bash
cd /tmp
git clone <repository-url> corporate-messenger
cd corporate-messenger
```

### Шаг 3: Запустите скрипт установки
```bash
chmod +x deploy-ubuntu.sh
sudo bash deploy-ubuntu.sh
```

Скрипт запросит:
- **Домен** (например: chat.example.com)
- **Email** для SSL сертификата

### Шаг 4: Готово!
После завершения установки (10-15 минут) приложение будет доступно по адресу:
- **URL**: https://ваш-домен.com
- **Логин**: admin
- **Пароль**: admin123

⚠️ **Обязательно смените пароль после первого входа!**

## 🔧 Ручная установка (Пошаговая)

Если вы хотите больше контроля над процессом установки:

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo systemctl start docker
```

### 3. Установка Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### 4. Установка Nginx
```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 5. Установка Certbot (для SSL)
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 6. Настройка Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 7. Клонирование проекта
```bash
sudo mkdir -p /opt/corporate-messenger
cd /opt/corporate-messenger
sudo git clone <repository-url> .
```

### 8. Настройка переменных окружения

#### Backend (.env)
```bash
cd /opt/corporate-messenger/backend
sudo cp .env.example .env
sudo nano .env
```

Измените:
```env
DATABASE_URL=postgresql://chatuser:STRONG_PASSWORD@postgres:5432/chatdb
SECRET_KEY=GENERATE_STRONG_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_FILE_SIZE=10485760
CORS_ORIGINS=https://ваш-домен.com
```

Генерация SECRET_KEY:
```bash
openssl rand -hex 32
```

#### Frontend (.env)
```bash
cd /opt/corporate-messenger/frontend
sudo cp .env.example .env
sudo nano .env
```

Измените:
```env
VITE_API_URL=https://ваш-домен.com/api
VITE_WS_URL=wss://ваш-домен.com
```

### 9. Создание Production Docker Compose

Создайте файл `docker-compose.prod.yml`:
```bash
sudo nano /opt/corporate-messenger/docker-compose.prod.yml
```

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
```

Создайте `.env.prod`:
```bash
echo "POSTGRES_PASSWORD=$(openssl rand -hex 16)" | sudo tee /opt/corporate-messenger/.env.prod
```

### 10. Настройка Nginx

Создайте конфигурацию:
```bash
sudo nano /etc/nginx/sites-available/chat
```

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=ws_limit:10m rate=5r/s;

server {
    listen 80;
    server_name ваш-домен.com;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name ваш-домен.com;

    ssl_certificate /etc/letsencrypt/live/ваш-домен.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ваш-домен.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        limit_req zone=ws_limit burst=10 nodelay;
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    location /docs {
        proxy_pass http://backend;
    }
}
```

Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/chat /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
```

### 11. Получение SSL сертификата
```bash
sudo certbot certonly --nginx -d ваш-домен.com --email ваш-email@example.com
sudo systemctl reload nginx
```

### 12. Запуск приложения
```bash
cd /opt/corporate-messenger
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

### 13. Применение миграций
```bash
sudo docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 14. Создание администратора
```bash
sudo docker-compose -f docker-compose.prod.yml exec backend python -c "
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
print('Администратор создан')
"
```

## 🔄 Автоматические бэкапы

### Создание скрипта бэкапа
```bash
sudo nano /opt/corporate-messenger/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/corporate-messenger/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"

mkdir -p "$BACKUP_DIR"

docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

find ${BACKUP_DIR} -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup created: ${BACKUP_FILE}"
```

```bash
sudo chmod +x /opt/corporate-messenger/backup.sh
```

### Настройка cron
```bash
sudo crontab -e
```

Добавьте:
```
# Бэкап каждый день в 2:00
0 2 * * * /opt/corporate-messenger/backup.sh >> /var/log/chat-backup.log 2>&1

# Обновление SSL каждое воскресенье
0 0 * * 0 certbot renew --quiet && systemctl reload nginx
```

## 🔧 Управление приложением

### Просмотр логов
```bash
# Все сервисы
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs -f

# Только backend
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs -f backend

# Последние 100 строк
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs --tail=100
```

### Перезапуск сервисов
```bash
# Все сервисы
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml restart

# Конкретный сервис
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml restart backend
```

### Остановка приложения
```bash
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml down
```

### Запуск приложения
```bash
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml up -d
```

### Обновление приложения
```bash
cd /opt/corporate-messenger
sudo docker-compose -f docker-compose.prod.yml down
sudo git pull origin main
sudo docker-compose -f docker-compose.prod.yml up -d --build
sudo docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Мониторинг ресурсов
```bash
# Использование ресурсов контейнерами
sudo docker stats

# Статус контейнеров
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml ps

# Проверка дискового пространства
df -h
```

## 🔒 Безопасность

### Настройка Fail2Ban
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Регулярные обновления
```bash
# Создайте скрипт обновления
sudo nano /opt/update-system.sh
```

```bash
#!/bin/bash
apt update
apt upgrade -y
apt autoremove -y
docker system prune -f
```

```bash
sudo chmod +x /opt/update-system.sh
```

Добавьте в cron (каждое воскресенье в 3:00):
```bash
sudo crontab -e
```

```
0 3 * * 0 /opt/update-system.sh >> /var/log/system-update.log 2>&1
```

### Смена паролей
После установки обязательно смените:
1. Пароль администратора в приложении
2. Пароль PostgreSQL в `.env` файлах
3. SECRET_KEY в backend/.env

## 🆘 Решение проблем

### Проблема: Контейнеры не запускаются
```bash
# Проверьте логи
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs

# Проверьте статус
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml ps

# Пересоздайте контейнеры
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml up -d --force-recreate
```

### Проблема: SSL сертификат не работает
```bash
# Проверьте сертификат
sudo certbot certificates

# Обновите сертификат
sudo certbot renew

# Перезапустите Nginx
sudo systemctl restart nginx
```

### Проблема: База данных недоступна
```bash
# Проверьте подключение
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec postgres psql -U chatuser -d chatdb

# Перезапустите БД
sudo docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml restart postgres
```

### Проблема: Высокая нагрузка
```bash
# Проверьте использование ресурсов
sudo docker stats

# Увеличьте ресурсы в docker-compose.prod.yml
# Добавьте в сервис backend:
resources:
  limits:
    cpus: '2'
    memory: 2G
```

### Проблема: Нет места на диске
```bash
# Очистите Docker
sudo docker system prune -a --volumes

# Удалите старые бэкапы
sudo find /opt/corporate-messenger/backups -name "backup_*.sql.gz" -mtime +7 -delete
```

## 📊 Мониторинг

### Простой мониторинг
```bash
# Создайте скрипт проверки
sudo nano /opt/check-health.sh
```

```bash
#!/bin/bash
echo "=== Статус контейнеров ==="
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml ps

echo ""
echo "=== Использование ресурсов ==="
docker stats --no-stream

echo ""
echo "=== Дисковое пространство ==="
df -h

echo ""
echo "=== Проверка доступности ==="
curl -s -o /dev/null -w "%{http_code}" https://ваш-домен.com
```

```bash
sudo chmod +x /opt/check-health.sh
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo docker-compose logs`
2. Проверьте статус: `sudo docker-compose ps`
3. Проверьте документацию: `README.md`, `DEPLOYMENT.md`
4. Создайте issue в GitHub

## ✅ Чеклист после установки

- [ ] Приложение доступно по HTTPS
- [ ] SSL сертификат работает
- [ ] Вход под admin работает
- [ ] Пароль администратора изменен
- [ ] Бэкапы настроены
- [ ] Firewall настроен
- [ ] Fail2Ban установлен
- [ ] Автообновление SSL настроено
- [ ] Мониторинг настроен

---

**Готово!** Ваш корпоративный мессенджер установлен и готов к работе! 🎉
