#!/bin/bash

# Скрипт проверки здоровья приложения
# Использование: bash check-health.sh

INSTALL_DIR="/opt/corporate-messenger"
DOMAIN="${1:-localhost}"

echo "================================================"
echo "  Проверка здоровья приложения"
echo "================================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция проверки
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi
}

# 1. Проверка Docker
echo -n "🐳 Docker: "
docker --version > /dev/null 2>&1
check_status $?

# 2. Проверка Docker Compose
echo -n "🐳 Docker Compose: "
docker-compose --version > /dev/null 2>&1
check_status $?

# 3. Проверка контейнеров
echo ""
echo "📦 Статус контейнеров:"
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    docker-compose -f docker-compose.prod.yml ps 2>/dev/null || docker-compose ps
else
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
fi

# 4. Проверка использования ресурсов
echo ""
echo "💻 Использование ресурсов:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# 5. Проверка дискового пространства
echo ""
echo "💾 Дисковое пространство:"
df -h | grep -E "Filesystem|/$|/opt"

# 6. Проверка Docker volumes
echo ""
echo "📁 Docker volumes:"
docker volume ls | grep -E "NAME|chat"

# 7. Проверка портов
echo ""
echo "🔌 Открытые порты:"
if command -v netstat > /dev/null 2>&1; then
    netstat -tlnp | grep -E "80|443|8000|3000|5432" || echo "Порты не найдены"
elif command -v ss > /dev/null 2>&1; then
    ss -tlnp | grep -E "80|443|8000|3000|5432" || echo "Порты не найдены"
fi

# 8. Проверка доступности приложения
echo ""
echo "🌐 Проверка доступности:"

# Backend API
echo -n "   Backend API (http://localhost:8000/api/health): "
if command -v curl > /dev/null 2>&1; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
        echo -e "${GREEN}✅ Доступен (HTTP $HTTP_CODE)${NC}"
    else
        echo -e "${RED}❌ Недоступен (HTTP $HTTP_CODE)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl не установлен${NC}"
fi

# Frontend
echo -n "   Frontend (http://localhost:3000): "
if command -v curl > /dev/null 2>&1; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✅ Доступен (HTTP $HTTP_CODE)${NC}"
    else
        echo -e "${RED}❌ Недоступен (HTTP $HTTP_CODE)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl не установлен${NC}"
fi

# HTTPS (если указан домен)
if [ "$DOMAIN" != "localhost" ]; then
    echo -n "   HTTPS (https://$DOMAIN): "
    if command -v curl > /dev/null 2>&1; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" = "200" ]; then
            echo -e "${GREEN}✅ Доступен (HTTP $HTTP_CODE)${NC}"
        else
            echo -e "${RED}❌ Недоступен (HTTP $HTTP_CODE)${NC}"
        fi
    fi
fi

# 9. Проверка логов на ошибки
echo ""
echo "📋 Последние ошибки в логах:"
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    echo "   Backend:"
    docker-compose -f docker-compose.prod.yml logs --tail=20 backend 2>/dev/null | grep -i "error" | tail -5 || echo "   Ошибок не найдено"
    echo ""
    echo "   Frontend:"
    docker-compose -f docker-compose.prod.yml logs --tail=20 frontend 2>/dev/null | grep -i "error" | tail -5 || echo "   Ошибок не найдено"
fi

# 10. Проверка бэкапов
echo ""
echo "💾 Последние бэкапы:"
if [ -d "$INSTALL_DIR/backups" ]; then
    ls -lht "$INSTALL_DIR/backups"/*.sql.gz 2>/dev/null | head -5 || echo "   Бэкапы не найдены"
else
    echo "   Директория бэкапов не найдена"
fi

# 11. Проверка SSL сертификата
if [ "$DOMAIN" != "localhost" ]; then
    echo ""
    echo "🔒 SSL сертификат:"
    if command -v openssl > /dev/null 2>&1; then
        echo "   Домен: $DOMAIN"
        CERT_INFO=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "$CERT_INFO" | sed 's/^/   /'
        else
            echo -e "   ${RED}❌ Не удалось получить информацию о сертификате${NC}"
        fi
    fi
fi

# 12. Системная информация
echo ""
echo "🖥️  Системная информация:"
echo "   OS: $(uname -s) $(uname -r)"
echo "   Uptime: $(uptime -p 2>/dev/null || uptime)"
echo "   Load Average: $(uptime | awk -F'load average:' '{print $2}')"

# 13. Рекомендации
echo ""
echo "================================================"
echo "  💡 Рекомендации"
echo "================================================"

# Проверка свободного места
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo -e "${RED}⚠️  Диск заполнен на ${DISK_USAGE}%! Рекомендуется очистка.${NC}"
    echo "   Команда: docker system prune -a --volumes"
fi

# Проверка памяти
MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 80 ]; then
    echo -e "${YELLOW}⚠️  Память используется на ${MEM_USAGE}%${NC}"
fi

# Проверка старых бэкапов
if [ -d "$INSTALL_DIR/backups" ]; then
    OLD_BACKUPS=$(find "$INSTALL_DIR/backups" -name "*.sql.gz" -mtime +30 | wc -l)
    if [ "$OLD_BACKUPS" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Найдено $OLD_BACKUPS старых бэкапов (>30 дней)${NC}"
        echo "   Команда: find $INSTALL_DIR/backups -name '*.sql.gz' -mtime +30 -delete"
    fi
fi

echo ""
echo "================================================"
echo ""
