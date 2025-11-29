#!/bin/bash

# Скрипт для загрузки изображений в production контейнер
# Запускать на сервере после загрузки uploads.zip

set -e

echo "========================================="
echo "📸 Загрузка изображений в контейнер"
echo "========================================="
echo ""

# Проверка наличия архива
if [ ! -f "uploads.zip" ]; then
    echo "❌ Файл uploads.zip не найден!"
    echo "Загрузите архив на сервер в /opt/edu-na-bazar/"
    exit 1
fi

# Проверка запущен ли контейнер
if ! docker ps | grep -q "edu-na-bazar-backend"; then
    echo "❌ Контейнер edu-na-bazar-backend не запущен!"
    echo "Запустите: docker-compose up -d"
    exit 1
fi

echo "📦 Копирование архива в контейнер..."
docker cp uploads.zip edu-na-bazar-backend:/tmp/

echo "📂 Распаковка архива..."
docker exec edu-na-bazar-backend unzip -o /tmp/uploads.zip -d /app/

echo "🗑️  Удаление временного архива..."
docker exec edu-na-bazar-backend rm /tmp/uploads.zip

echo "🔧 Установка прав доступа..."
docker exec edu-na-bazar-backend chmod -R 755 /app/uploads/

echo ""
echo "========================================="
echo "✅ Изображения успешно загружены!"
echo "========================================="
echo ""

# Подсчет файлов
FILE_COUNT=$(docker exec edu-na-bazar-backend find /app/uploads/products/original/ -type f | wc -l)
echo "📊 Загружено файлов: $FILE_COUNT"
echo ""

# Проверка доступа
echo "🔍 Проверка доступа к изображениям..."
FIRST_IMAGE=$(docker exec edu-na-bazar-backend ls /app/uploads/products/original/ | head -1)

if [ -n "$FIRST_IMAGE" ]; then
    echo "   Тестовый файл: $FIRST_IMAGE"
    
    # Проверка через API
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/uploads/products/original/$FIRST_IMAGE)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "   ✅ API доступ: OK (HTTP $HTTP_CODE)"
    else
        echo "   ⚠️  API доступ: FAILED (HTTP $HTTP_CODE)"
    fi
else
    echo "   ⚠️  Файлы не найдены!"
fi

echo ""
echo "🎉 Готово! Проверьте отображение изображений на сайте."
echo ""
