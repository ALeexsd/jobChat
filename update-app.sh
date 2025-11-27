#!/bin/bash

# Скрипт обновления приложения на production сервере
# Использование: sudo bash update-app.sh

set -e

INSTALL_DIR="/opt/corporate-messenger"

echo "================================================"
echo "  Обновление корпоративного мессенджера"
echo "================================================"
echo ""

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Запустите скрипт с правами root: sudo bash update-app.sh"
    exit 1
fi

# Проверка существования директории
if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ Директория $INSTALL_DIR не найдена!"
    echo "   Возможно приложение не установлено."
    exit 1
fi

cd "$INSTALL_DIR"

echo "🔄 Шаг 1/6: Создание бэкапа..."
BACKUP_DIR="$INSTALL_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_before_update_${DATE}.sql.gz"

mkdir -p "$BACKUP_DIR"

docker-compose -f docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

echo "✅ Бэкап создан: ${BACKUP_FILE}"

echo ""
echo "🔄 Шаг 2/6: Остановка сервисов..."
docker-compose -f docker-compose.prod.yml down

echo ""
echo "🔄 Шаг 3/6: Обновление кода..."
git fetch origin
git pull origin main

echo ""
echo "🔄 Шаг 4/6: Пересборка образов..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo ""
echo "🔄 Шаг 5/6: Запуск сервисов..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Ожидание запуска сервисов (20 секунд)..."
sleep 20

echo ""
echo "🔄 Шаг 6/6: Применение миграций..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

echo ""
echo "================================================"
echo "  ✅ Обновление завершено успешно!"
echo "================================================"
echo ""
echo "📋 Информация:"
echo "   Бэкап: ${BACKUP_FILE}"
echo "   Статус: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml ps"
echo "   Логи: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml logs -f"
echo ""
