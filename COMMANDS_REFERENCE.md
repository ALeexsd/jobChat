# 🔧 Справочник команд

Быстрая справка по всем командам для управления приложением на VPS.

## 🚀 Установка

```bash
# Автоматическая установка
cd /tmp
git clone <repository-url> corporate-messenger
cd corporate-messenger
chmod +x deploy-ubuntu.sh
sudo bash deploy-ubuntu.sh
```

## 📊 Управление приложением

### Быстрые команды (алиасы)

```bash
chat-status      # Статус контейнеров
chat-logs        # Просмотр логов в реальном времени
chat-restart     # Перезапуск всех сервисов
chat-stop        # Остановка всех сервисов
chat-start       # Запуск всех сервисов
chat-backup      # Создать бэкап БД
chat-health      # Проверка здоровья системы
chat-dashboard   # Интерактивный dashboard
chat-monitor     # Запустить мониторинг вручную
```

### Docker Compose команды

```bash
cd /opt/corporate-messenger

# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Логи всех сервисов
docker-compose -f docker-compose.prod.yml logs -f

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres

# Последние N строк логов
docker-compose -f docker-compose.prod.yml logs --tail=100 backend

# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart backend

# Остановка
docker-compose -f docker-compose.prod.yml down

# Запуск
docker-compose -f docker-compose.prod.yml up -d

# Пересоздание контейнеров
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Пересборка образов
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

## 🐳 Docker команды

```bash
# Список всех контейнеров
docker ps -a

# Статистика использования ресурсов
docker stats

# Логи контейнера
docker logs chat_backend -f
docker logs chat_frontend -f
docker logs chat_postgres -f

# Выполнение команды в контейнере
docker exec -it chat_backend bash
docker exec -it chat_postgres psql -U chatuser -d chatdb

# Остановка контейнера
docker stop chat_backend

# Запуск контейнера
docker start chat_backend

# Перезапуск контейнера
docker restart chat_backend

# Удаление контейнера
docker rm -f chat_backend

# Список образов
docker images

# Удаление образа
docker rmi image_name

# Очистка неиспользуемых ресурсов
docker system prune -a --volumes
```

## 💾 Бэкапы

```bash
# Создать бэкап
/opt/corporate-messenger/backup.sh
# или
chat-backup

# Список бэкапов
ls -lh /opt/corporate-messenger/backups/

# Восстановить из бэкапа
cd /opt/corporate-messenger
sudo bash restore-backup.sh backups/backup_20240101_120000.sql.gz

# Удалить старые бэкапы (>30 дней)
find /opt/corporate-messenger/backups -name "*.sql.gz" -mtime +30 -delete

# Ручной бэкап PostgreSQL
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > backup_manual.sql.gz
```

## 🔄 Обновление

```bash
# Автоматическое обновление
cd /opt/corporate-messenger
sudo bash update-app.sh

# Ручное обновление
cd /opt/corporate-messenger
docker-compose -f docker-compose.prod.yml down
git pull origin main
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## 🗄️ База данных

```bash
# Подключение к PostgreSQL
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec postgres \
    psql -U chatuser -d chatdb

# Список таблиц
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec postgres \
    psql -U chatuser -d chatdb -c "\dt"

# Выполнение SQL запроса
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec postgres \
    psql -U chatuser -d chatdb -c "SELECT COUNT(*) FROM users;"

# Применение миграций
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec backend \
    alembic upgrade head

# Откат миграции
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec backend \
    alembic downgrade -1

# История миграций
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec backend \
    alembic history
```

## 🌐 Nginx

```bash
# Проверка конфигурации
sudo nginx -t

# Перезагрузка конфигурации
sudo nginx -s reload
sudo systemctl reload nginx

# Перезапуск Nginx
sudo systemctl restart nginx

# Статус Nginx
sudo systemctl status nginx

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Редактирование конфигурации
sudo nano /etc/nginx/sites-available/chat
```

## 🔒 SSL сертификаты

```bash
# Список сертификатов
sudo certbot certificates

# Обновление сертификата
sudo certbot renew

# Принудительное обновление
sudo certbot renew --force-renewal

# Получение нового сертификата
sudo certbot certonly --nginx -d ваш-домен.com

# Удаление сертификата
sudo certbot delete --cert-name ваш-домен.com

# Тест автообновления
sudo certbot renew --dry-run
```

## 🔥 Firewall (UFW)

```bash
# Статус firewall
sudo ufw status

# Включить firewall
sudo ufw enable

# Отключить firewall
sudo ufw disable

# Разрешить порт
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Запретить порт
sudo ufw deny 8080/tcp

# Удалить правило
sudo ufw delete allow 8080/tcp

# Сброс правил
sudo ufw reset
```

## 📊 Мониторинг

```bash
# Проверка здоровья
/opt/check-health.sh
# или
chat-health

# Dashboard
/opt/dashboard.sh
# или
chat-dashboard

# Ручной запуск мониторинга
/opt/monitor-chat.sh
# или
chat-monitor

# Ежедневный отчет
/opt/daily-report.sh

# Просмотр логов мониторинга
tail -f /var/log/chat-monitor.log
tail -f /var/log/chat-backup.log
```

## 💻 Системные команды

```bash
# Использование диска
df -h

# Использование памяти
free -h

# Использование CPU
top
htop

# Процессы
ps aux | grep docker
ps aux | grep nginx

# Сетевые подключения
netstat -tlnp
ss -tlnp

# Открытые порты
sudo netstat -tlnp | grep -E "80|443|8000|3000|5432"

# Uptime
uptime

# Системная информация
uname -a
lsb_release -a
```

## 🧹 Очистка

```bash
# Очистка Docker
docker system prune -a --volumes

# Очистка логов Docker
truncate -s 0 /var/lib/docker/containers/*/*-json.log

# Очистка старых бэкапов
find /opt/corporate-messenger/backups -name "*.sql.gz" -mtime +30 -delete

# Очистка системных логов
sudo truncate -s 0 /var/log/syslog
sudo truncate -s 0 /var/log/kern.log

# Очистка apt кэша
sudo apt clean
sudo apt autoremove -y

# Очистка журналов systemd
sudo journalctl --vacuum-time=7d
```

## 🔧 Конфигурация

```bash
# Редактирование backend .env
sudo nano /opt/corporate-messenger/backend/.env

# Редактирование frontend .env
sudo nano /opt/corporate-messenger/frontend/.env

# Редактирование docker-compose
sudo nano /opt/corporate-messenger/docker-compose.prod.yml

# Редактирование Nginx конфигурации
sudo nano /etc/nginx/sites-available/chat

# Просмотр cron задач
crontab -l

# Редактирование cron задач
crontab -e
```

## 🔐 Безопасность

```bash
# Генерация SECRET_KEY
openssl rand -hex 32

# Генерация пароля
openssl rand -base64 32

# Проверка открытых портов
sudo netstat -tlnp

# Fail2Ban статус
sudo systemctl status fail2ban

# Fail2Ban логи
sudo tail -f /var/log/fail2ban.log

# SSH конфигурация
sudo nano /etc/ssh/sshd_config
sudo systemctl restart sshd
```

## 📝 Логи

```bash
# Логи приложения
chat-logs

# Логи backend
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs -f backend

# Логи frontend
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs -f frontend

# Логи PostgreSQL
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs -f postgres

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Системные логи
sudo tail -f /var/log/syslog

# Логи мониторинга
tail -f /var/log/chat-monitor.log
tail -f /var/log/chat-backup.log

# Поиск ошибок в логах
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs backend | grep -i error
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs backend | grep -i critical
```

## 🆘 Решение проблем

```bash
# Полная перезагрузка
cd /opt/corporate-messenger
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Пересборка всего
cd /opt/corporate-messenger
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Проверка подключения к БД
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml exec postgres \
    psql -U chatuser -d chatdb -c "SELECT 1;"

# Проверка backend API
curl http://localhost:8000/api/health

# Проверка frontend
curl http://localhost:3000

# Проверка HTTPS
curl -I https://ваш-домен.com

# Перезагрузка сервера (крайний случай)
sudo reboot
```

## 📞 Полезные команды

```bash
# Быстрая диагностика
chat-health && chat-status && docker stats --no-stream

# Полная информация о системе
chat-dashboard

# Создать бэкап и проверить
chat-backup && ls -lh /opt/corporate-messenger/backups/ | tail -1

# Проверить все логи на ошибки
docker-compose -f /opt/corporate-messenger/docker-compose.prod.yml logs --tail=100 | grep -i "error\|critical\|fatal"

# Мониторинг в реальном времени
watch -n 5 'docker stats --no-stream'
```

---

## 💡 Советы

### Создание алиасов
Добавьте в `~/.bashrc`:
```bash
alias logs='chat-logs'
alias status='chat-status'
alias restart='chat-restart'
```

### Быстрый доступ
```bash
# Создайте симлинк
ln -s /opt/corporate-messenger ~/chat
cd ~/chat
```

### Мониторинг в tmux
```bash
# Установка tmux
sudo apt install tmux -y

# Создание сессии
tmux new -s monitoring

# Разделение окна
Ctrl+B, затем %  # вертикально
Ctrl+B, затем "  # горизонтально

# В разных панелях:
chat-logs
docker stats
htop
```

---

**Сохраните этот файл для быстрого доступа к командам!**
