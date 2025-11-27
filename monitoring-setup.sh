#!/bin/bash

# Скрипт настройки мониторинга и алертов
# Использование: sudo bash monitoring-setup.sh

set -e

INSTALL_DIR="/opt/corporate-messenger"
EMAIL="${1}"

echo "================================================"
echo "  Настройка мониторинга"
echo "================================================"
echo ""

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Запустите скрипт с правами root: sudo bash monitoring-setup.sh your@email.com"
    exit 1
fi

# Проверка email
if [ -z "$EMAIL" ]; then
    read -p "Введите email для уведомлений: " EMAIL
fi

if [ -z "$EMAIL" ]; then
    echo "❌ Email обязателен!"
    exit 1
fi

echo "📧 Email для уведомлений: $EMAIL"
echo ""

# 1. Установка необходимых пакетов
echo "🔄 Установка пакетов для мониторинга..."
apt update
apt install -y mailutils sysstat htop

# 2. Создание скрипта мониторинга
echo ""
echo "🔄 Создание скрипта мониторинга..."

cat > /opt/monitor-chat.sh << 'EOFMONITOR'
#!/bin/bash

# Конфигурация
EMAIL="EMAIL_PLACEHOLDER"
INSTALL_DIR="/opt/corporate-messenger"
LOG_FILE="/var/log/chat-monitor.log"
ALERT_FILE="/tmp/chat-alert-sent"

# Функция отправки алерта
send_alert() {
    local subject="$1"
    local message="$2"
    
    # Проверяем, не отправляли ли мы уже алерт в последний час
    if [ -f "$ALERT_FILE" ]; then
        LAST_ALERT=$(stat -c %Y "$ALERT_FILE")
        CURRENT_TIME=$(date +%s)
        DIFF=$((CURRENT_TIME - LAST_ALERT))
        
        if [ $DIFF -lt 3600 ]; then
            echo "$(date): Алерт пропущен (отправлен менее часа назад)" >> "$LOG_FILE"
            return
        fi
    fi
    
    echo "$message" | mail -s "$subject" "$EMAIL"
    touch "$ALERT_FILE"
    echo "$(date): Алерт отправлен: $subject" >> "$LOG_FILE"
}

# Проверка контейнеров
check_containers() {
    cd "$INSTALL_DIR"
    
    CONTAINERS=("chat_postgres" "chat_backend" "chat_frontend")
    
    for container in "${CONTAINERS[@]}"; do
        if ! docker ps | grep -q "$container"; then
            send_alert "🚨 Контейнер $container не запущен!" \
                "Контейнер $container остановлен или недоступен.\n\nВремя: $(date)\n\nПопытка перезапуска..."
            
            # Попытка перезапуска
            docker-compose -f docker-compose.prod.yml restart "$container" || true
        fi
    done
}

# Проверка использования диска
check_disk() {
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$DISK_USAGE" -gt 85 ]; then
        send_alert "🚨 Диск заполнен на ${DISK_USAGE}%!" \
            "Критический уровень использования диска: ${DISK_USAGE}%\n\nВремя: $(date)\n\nРекомендуется очистка."
    fi
}

# Проверка использования памяти
check_memory() {
    MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
    
    if [ "$MEM_USAGE" -gt 90 ]; then
        send_alert "🚨 Память используется на ${MEM_USAGE}%!" \
            "Критический уровень использования памяти: ${MEM_USAGE}%\n\nВремя: $(date)"
    fi
}

# Проверка доступности приложения
check_availability() {
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "404" ]; then
        send_alert "🚨 Backend недоступен!" \
            "Backend API не отвечает (HTTP $HTTP_CODE)\n\nВремя: $(date)\n\nПопытка перезапуска..."
        
        cd "$INSTALL_DIR"
        docker-compose -f docker-compose.prod.yml restart backend || true
    fi
}

# Проверка логов на критические ошибки
check_logs() {
    cd "$INSTALL_DIR"
    
    ERRORS=$(docker-compose -f docker-compose.prod.yml logs --tail=100 backend 2>/dev/null | grep -i "critical\|fatal" | wc -l)
    
    if [ "$ERRORS" -gt 5 ]; then
        LAST_ERRORS=$(docker-compose -f docker-compose.prod.yml logs --tail=10 backend 2>/dev/null | grep -i "critical\|fatal")
        send_alert "🚨 Обнаружены критические ошибки!" \
            "Найдено $ERRORS критических ошибок в логах backend\n\nПоследние ошибки:\n$LAST_ERRORS\n\nВремя: $(date)"
    fi
}

# Проверка бэкапов
check_backups() {
    BACKUP_DIR="$INSTALL_DIR/backups"
    
    if [ -d "$BACKUP_DIR" ]; then
        LAST_BACKUP=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
        
        if [ -n "$LAST_BACKUP" ]; then
            BACKUP_AGE=$(( ($(date +%s) - $(stat -c %Y "$LAST_BACKUP")) / 86400 ))
            
            if [ "$BACKUP_AGE" -gt 2 ]; then
                send_alert "⚠️ Бэкап устарел!" \
                    "Последний бэкап был создан $BACKUP_AGE дней назад\n\nФайл: $LAST_BACKUP\n\nВремя: $(date)"
            fi
        else
            send_alert "⚠️ Бэкапы не найдены!" \
                "В директории $BACKUP_DIR не найдено бэкапов\n\nВремя: $(date)"
        fi
    fi
}

# Запуск всех проверок
echo "$(date): Запуск мониторинга..." >> "$LOG_FILE"

check_containers
check_disk
check_memory
check_availability
check_logs
check_backups

echo "$(date): Мониторинг завершен" >> "$LOG_FILE"
EOFMONITOR

# Замена email в скрипте
sed -i "s/EMAIL_PLACEHOLDER/$EMAIL/g" /opt/monitor-chat.sh
chmod +x /opt/monitor-chat.sh

# 3. Создание скрипта ежедневного отчета
echo ""
echo "🔄 Создание скрипта ежедневного отчета..."

cat > /opt/daily-report.sh << 'EOFREPORT'
#!/bin/bash

EMAIL="EMAIL_PLACEHOLDER"
INSTALL_DIR="/opt/corporate-messenger"

# Генерация отчета
REPORT=$(cat << EOF
📊 Ежедневный отчет - $(date +"%d.%m.%Y")

🐳 Статус контейнеров:
$(cd $INSTALL_DIR && docker-compose -f docker-compose.prod.yml ps)

💻 Использование ресурсов:
$(docker stats --no-stream --format "{{.Name}}: CPU {{.CPUPerc}}, Memory {{.MemUsage}}")

💾 Дисковое пространство:
$(df -h / | grep -v Filesystem)

📦 Docker volumes:
$(docker volume ls | grep chat)

💾 Последние бэкапы:
$(ls -lht $INSTALL_DIR/backups/*.sql.gz 2>/dev/null | head -3 || echo "Бэкапы не найдены")

📋 Статистика логов (последние 24 часа):
Ошибки: $(cd $INSTALL_DIR && docker-compose -f docker-compose.prod.yml logs --since 24h backend 2>/dev/null | grep -i "error" | wc -l)
Предупреждения: $(cd $INSTALL_DIR && docker-compose -f docker-compose.prod.yml logs --since 24h backend 2>/dev/null | grep -i "warning" | wc -l)

🖥️ Системная информация:
Uptime: $(uptime -p)
Load Average: $(uptime | awk -F'load average:' '{print $2}')
Memory: $(free -h | awk 'NR==2 {print $3 "/" $2}')

---
Автоматический отчет системы мониторинга
EOF
)

echo "$REPORT" | mail -s "📊 Ежедневный отчет - $(date +"%d.%m.%Y")" "$EMAIL"
EOFREPORT

sed -i "s/EMAIL_PLACEHOLDER/$EMAIL/g" /opt/daily-report.sh
chmod +x /opt/daily-report.sh

# 4. Настройка cron
echo ""
echo "🔄 Настройка cron задач..."

# Удаляем старые задачи мониторинга если есть
crontab -l 2>/dev/null | grep -v "monitor-chat.sh" | grep -v "daily-report.sh" | crontab - || true

# Добавляем новые задачи
(crontab -l 2>/dev/null; echo "# Мониторинг каждые 5 минут") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/monitor-chat.sh") | crontab -
(crontab -l 2>/dev/null; echo "# Ежедневный отчет в 9:00") | crontab -
(crontab -l 2>/dev/null; echo "0 9 * * * /opt/daily-report.sh") | crontab -

# 5. Создание dashboard скрипта
echo ""
echo "🔄 Создание dashboard..."

cat > /opt/dashboard.sh << 'EOFDASH'
#!/bin/bash

INSTALL_DIR="/opt/corporate-messenger"

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  📊 Dashboard корпоративного мессенджера${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Статус контейнеров
echo -e "${GREEN}🐳 Контейнеры:${NC}"
cd "$INSTALL_DIR"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo -e "${GREEN}💻 Ресурсы:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo -e "${GREEN}💾 Диск:${NC}"
df -h / | grep -E "Filesystem|/$"

echo ""
echo -e "${GREEN}📊 Системная информация:${NC}"
echo "  Uptime: $(uptime -p)"
echo "  Load: $(uptime | awk -F'load average:' '{print $2}')"
echo "  Memory: $(free -h | awk 'NR==2 {print $3 "/" $2}')"

echo ""
echo -e "${GREEN}💾 Последние бэкапы:${NC}"
ls -lht "$INSTALL_DIR/backups"/*.sql.gz 2>/dev/null | head -3 || echo "  Бэкапы не найдены"

echo ""
echo -e "${GREEN}📋 Последние логи (backend):${NC}"
docker-compose -f docker-compose.prod.yml logs --tail=5 backend

echo ""
echo -e "${BLUE}================================================${NC}"
echo ""
EOFDASH

chmod +x /opt/dashboard.sh

# 6. Создание алиасов
echo ""
echo "🔄 Создание удобных команд..."

cat >> /root/.bashrc << 'EOFALIAS'

# Корпоративный мессенджер - удобные команды
alias chat-status='cd /opt/corporate-messenger && docker-compose -f docker-compose.prod.yml ps'
alias chat-logs='cd /opt/corporate-messenger && docker-compose -f docker-compose.prod.yml logs -f'
alias chat-restart='cd /opt/corporate-messenger && docker-compose -f docker-compose.prod.yml restart'
alias chat-stop='cd /opt/corporate-messenger && docker-compose -f docker-compose.prod.yml down'
alias chat-start='cd /opt/corporate-messenger && docker-compose -f docker-compose.prod.yml up -d'
alias chat-backup='/opt/corporate-messenger/backup.sh'
alias chat-monitor='/opt/monitor-chat.sh'
alias chat-dashboard='/opt/dashboard.sh'
alias chat-health='/opt/check-health.sh'
EOFALIAS

source /root/.bashrc

# 7. Тестовый запуск
echo ""
echo "🔄 Тестовый запуск мониторинга..."
/opt/monitor-chat.sh

echo ""
echo "================================================"
echo "  ✅ Мониторинг настроен успешно!"
echo "================================================"
echo ""
echo "📧 Уведомления будут отправляться на: $EMAIL"
echo ""
echo "📋 Созданные скрипты:"
echo "   /opt/monitor-chat.sh - проверка каждые 5 минут"
echo "   /opt/daily-report.sh - ежедневный отчет в 9:00"
echo "   /opt/dashboard.sh - интерактивный dashboard"
echo ""
echo "🔧 Удобные команды:"
echo "   chat-status      - статус контейнеров"
echo "   chat-logs        - просмотр логов"
echo "   chat-restart     - перезапуск"
echo "   chat-stop        - остановка"
echo "   chat-start       - запуск"
echo "   chat-backup      - создать бэкап"
echo "   chat-monitor     - запустить мониторинг"
echo "   chat-dashboard   - показать dashboard"
echo "   chat-health      - проверка здоровья"
echo ""
echo "📊 Для просмотра dashboard выполните:"
echo "   chat-dashboard"
echo ""
echo "================================================"
