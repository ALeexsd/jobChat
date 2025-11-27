#!/bin/bash

# Скрипт восстановления из бэкапа
# Использование: sudo bash restore-backup.sh backup_file.sql.gz

set -e

INSTALL_DIR="/opt/corporate-messenger"
BACKUP_DIR="$INSTALL_DIR/backups"

echo "================================================"
echo "  Восстановление из бэкапа"
echo "================================================"
echo ""

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Запустите скрипт с правами root: sudo bash restore-backup.sh backup_file.sql.gz"
    exit 1
fi

# Проверка аргумента
if [ -z "$1" ]; then
    echo "❌ Укажите файл бэкапа!"
    echo ""
    echo "Использование: sudo bash restore-backup.sh backup_file.sql.gz"
    echo ""
    echo "Доступные бэкапы:"
    ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null || echo "  Бэкапы не найдены"
    exit 1
fi

BACKUP_FILE="$1"

# Проверка существования файла
if [ ! -f "$BACKUP_FILE" ]; then
    # Попробуем найти в директории бэкапов
    if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
        BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE"
    else
        echo "❌ Файл бэкапа не найден: $BACKUP_FILE"
        exit 1
    fi
fi

echo "📋 Параметры восстановления:"
echo "   Файл бэкапа: $BACKUP_FILE"
echo "   Размер: $(du -h "$BACKUP_FILE" | cut -f1)"
echo ""
read -p "Продолжить? Текущие данные будут удалены! (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Отменено"
    exit 1
fi

cd "$INSTALL_DIR"

echo ""
echo "🔄 Шаг 1/5: Создание бэкапа текущей БД..."
DATE=$(date +%Y%m%d_%H%M%S)
SAFETY_BACKUP="backup_before_restore_${DATE}.sql.gz"

docker-compose -f docker-compose.prod.yml exec -T postgres \
    pg_dump -U chatuser chatdb | gzip > "${BACKUP_DIR}/${SAFETY_BACKUP}"

echo "✅ Страховочный бэкап создан: ${SAFETY_BACKUP}"

echo ""
echo "🔄 Шаг 2/5: Остановка backend..."
docker-compose -f docker-compose.prod.yml stop backend

echo ""
echo "🔄 Шаг 3/5: Удаление текущей БД..."
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U chatuser -d postgres -c "DROP DATABASE IF EXISTS chatdb;"
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U chatuser -d postgres -c "CREATE DATABASE chatdb;"

echo ""
echo "🔄 Шаг 4/5: Восстановление из бэкапа..."
gunzip -c "$BACKUP_FILE" | docker-compose -f docker-compose.prod.yml exec -T postgres psql -U chatuser -d chatdb

echo ""
echo "🔄 Шаг 5/5: Запуск backend..."
docker-compose -f docker-compose.prod.yml start backend

echo ""
echo "⏳ Ожидание запуска (10 секунд)..."
sleep 10

echo ""
echo "================================================"
echo "  ✅ Восстановление завершено успешно!"
echo "================================================"
echo ""
echo "📋 Информация:"
echo "   Восстановлено из: $BACKUP_FILE"
echo "   Страховочный бэкап: ${SAFETY_BACKUP}"
echo ""
echo "🔧 Проверьте работу приложения:"
echo "   Статус: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml ps"
echo "   Логи: docker-compose -f $INSTALL_DIR/docker-compose.prod.yml logs -f backend"
echo ""
