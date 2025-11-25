#!/bin/bash

# Скрипт диагностики production сервера
# Использование: bash diagnose.sh

echo "🔍 Диагностика production сервера - Еду на базар"
echo "=================================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка 1: Docker контейнеры
echo "1️⃣  Проверка Docker контейнеров..."
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Контейнеры запущены${NC}"
    docker-compose ps
else
    echo -e "${RED}❌ Контейнеры не запущены${NC}"
    echo "Запустите: docker-compose up -d"
    exit 1
fi
echo ""

# Проверка 2: PostgreSQL
echo "2️⃣  Проверка PostgreSQL..."
if docker exec edu-na-bazar-postgres-1 pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL работает${NC}"
else
    echo -e "${RED}❌ PostgreSQL не отвечает${NC}"
    echo "Проверьте логи: docker-compose logs postgres"
    exit 1
fi
echo ""

# Проверка 3: База данных
echo "3️⃣  Проверка базы данных..."
DB_EXISTS=$(docker exec edu-na-bazar-postgres-1 psql -U postgres -lqt | cut -d \| -f 1 | grep -w edu_na_bazar | wc -l)
if [ "$DB_EXISTS" -eq 1 ]; then
    echo -e "${GREEN}✅ База данных edu_na_bazar существует${NC}"
else
    echo -e "${RED}❌ База данных edu_na_bazar не найдена${NC}"
    echo "Создайте БД: docker exec -it edu-na-bazar-postgres-1 psql -U postgres -c 'CREATE DATABASE edu_na_bazar;'"
    exit 1
fi
echo ""

# Проверка 4: Схемы
echo "4️⃣  Проверка схем..."
SCHEMAS=$(docker exec edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -t -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('market', 'config')" | grep -v '^$' | wc -l)
if [ "$SCHEMAS" -eq 2 ]; then
    echo -e "${GREEN}✅ Схемы market и config существуют${NC}"
else
    echo -e "${YELLOW}⚠️  Схемы не найдены - нужны миграции${NC}"
    echo "Примените миграции: docker-compose exec backend alembic upgrade head"
fi
echo ""

# Проверка 5: Таблицы
echo "5️⃣  Проверка таблиц..."
TABLES=$(docker exec edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'market'" 2>/dev/null)
if [ "$TABLES" -gt 0 ]; then
    echo -e "${GREEN}✅ Таблицы в схеме market: $TABLES${NC}"
    
    # Проверка данных
    CATEGORIES=$(docker exec edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -t -c "SELECT COUNT(*) FROM market.categories" 2>/dev/null | tr -d ' ')
    PRODUCTS=$(docker exec edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -t -c "SELECT COUNT(*) FROM market.products" 2>/dev/null | tr -d ' ')
    
    echo "   📊 Категорий: $CATEGORIES"
    echo "   📦 Товаров: $PRODUCTS"
    
    if [ "$CATEGORIES" -eq 0 ] || [ "$PRODUCTS" -eq 0 ]; then
        echo -e "${YELLOW}⚠️  БД пустая - нужно загрузить данные${NC}"
    fi
else
    echo -e "${RED}❌ Таблицы не найдены${NC}"
    echo "Примените миграции: docker-compose exec backend alembic upgrade head"
fi
echo ""

# Проверка 6: Версия миграций
echo "6️⃣  Проверка миграций Alembic..."
MIGRATION=$(docker-compose exec -T backend alembic current 2>/dev/null | grep -o '[a-f0-9]\{12\}')
if [ ! -z "$MIGRATION" ]; then
    echo -e "${GREEN}✅ Текущая миграция: $MIGRATION${NC}"
    if [ "$MIGRATION" == "8828a8665651" ]; then
        echo -e "${GREEN}✅ Миграции актуальны (head)${NC}"
    else
        echo -e "${YELLOW}⚠️  Миграция не актуальна${NC}"
        echo "Обновите: docker-compose exec backend alembic upgrade head"
    fi
else
    echo -e "${RED}❌ Миграции не применены${NC}"
    echo "Примените: docker-compose exec backend alembic upgrade head"
fi
echo ""

# Проверка 7: Backend health
echo "7️⃣  Проверка Backend API..."
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
if echo "$HEALTH" | grep -q "ok"; then
    echo -e "${GREEN}✅ Health endpoint работает${NC}"
    echo "   Response: $HEALTH"
else
    echo -e "${RED}❌ Health endpoint не отвечает${NC}"
    echo "Проверьте логи: docker-compose logs backend --tail=50"
fi
echo ""

# Проверка 8: API Categories
echo "8️⃣  Проверка API /api/categories/..."
CATEGORIES_API=$(curl -s http://localhost:8000/api/categories/ 2>/dev/null)
if echo "$CATEGORIES_API" | grep -q "id"; then
    echo -e "${GREEN}✅ API categories работает${NC}"
    COUNT=$(echo "$CATEGORIES_API" | grep -o '"id"' | wc -l)
    echo "   Категорий в ответе: $COUNT"
else
    echo -e "${RED}❌ API categories возвращает ошибку${NC}"
    echo "   Response: $CATEGORIES_API"
    echo ""
    echo "Последние логи backend:"
    docker-compose logs backend --tail=20
fi
echo ""

# Проверка 9: .env файл
echo "9️⃣  Проверка .env файла..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env файл существует${NC}"
    
    # Проверка критичных переменных
    if grep -q "SECRET_KEY=your-secret-key" .env; then
        echo -e "${YELLOW}⚠️  SECRET_KEY использует дефолтное значение${NC}"
    fi
    
    if grep -q "POSTGRES_PASSWORD=postgres" .env; then
        echo -e "${YELLOW}⚠️  POSTGRES_PASSWORD использует слабый пароль${NC}"
    fi
else
    echo -e "${RED}❌ .env файл не найден${NC}"
    echo "Создайте: cp .env.example .env"
fi
echo ""

# Проверка 10: Firewall
echo "🔟 Проверка firewall..."
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status | grep "8000/tcp" | grep "ALLOW")
    if [ ! -z "$UFW_STATUS" ]; then
        echo -e "${GREEN}✅ Порт 8000 открыт${NC}"
    else
        echo -e "${YELLOW}⚠️  Порт 8000 может быть закрыт${NC}"
        echo "Откройте: ufw allow 8000/tcp"
    fi
else
    echo -e "${YELLOW}⚠️  UFW не установлен${NC}"
fi
echo ""

# Итоговый результат
echo "=================================================="
echo "📊 ИТОГОВЫЙ РЕЗУЛЬТАТ"
echo "=================================================="

# Подсчет проблем
ERRORS=0
WARNINGS=0

# Логика подсчета на основе проверок выше
if ! docker-compose ps | grep -q "Up"; then ((ERRORS++)); fi
if ! docker exec edu-na-bazar-postgres-1 pg_isready -U postgres > /dev/null 2>&1; then ((ERRORS++)); fi
if [ "$DB_EXISTS" -ne 1 ]; then ((ERRORS++)); fi
if [ "$SCHEMAS" -ne 2 ]; then ((WARNINGS++)); fi
if [ "$TABLES" -eq 0 ]; then ((ERRORS++)); fi
if [ -z "$MIGRATION" ]; then ((ERRORS++)); fi
if ! echo "$HEALTH" | grep -q "ok"; then ((ERRORS++)); fi
if ! echo "$CATEGORIES_API" | grep -q "id"; then ((ERRORS++)); fi

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Все проверки пройдены!${NC}"
    echo ""
    echo "Сервер готов к работе:"
    echo "  - Frontend: http://176.99.5.211"
    echo "  - Backend: http://176.99.5.211:8000"
    echo "  - API Docs: http://176.99.5.211:8000/docs"
else
    echo -e "${RED}❌ Найдено ошибок: $ERRORS${NC}"
    echo -e "${YELLOW}⚠️  Предупреждений: $WARNINGS${NC}"
    echo ""
    echo "Рекомендуемые действия:"
    echo "  1. Проверьте логи: docker-compose logs backend --tail=50"
    echo "  2. Примените миграции: docker-compose exec backend alembic upgrade head"
    echo "  3. Проверьте .env файл"
    echo "  4. Перезапустите контейнеры: docker-compose restart"
fi

echo ""
echo "Для подробной информации см. DEBUG_500_ERROR.md"
