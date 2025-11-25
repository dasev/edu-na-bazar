# 🚀 Чек-лист деплоя на production сервер

## 📋 Информация о сервере
- **IP**: 176.99.5.211
- **User**: root
- **Password**: sIAS6APDsKh0bL
- **Готовность**: 90%

---

## ✅ Что уже готово локально

### 1. Backend работает
- ✅ FastAPI запущен на порту 8000
- ✅ БД PostgreSQL подключена и работает
- ✅ Redis работает
- ✅ Миграции Alembic применены (версия: 8828a8665651)
- ✅ Данные в БД: 22 товара, категории, магазины
- ✅ Health endpoint: http://localhost:8000/health → {"status":"ok"}

### 2. Frontend работает
- ✅ React приложение запущено на порту 3000
- ✅ Подключается к backend через http://localhost:8000

### 3. Docker контейнеры
- ✅ edu-na-bazar-postgres-dev (healthy)
- ✅ edu-na-bazar-redis-dev (healthy)
- ✅ edu-na-bazar-backend-dev (running)
- ✅ edu-na-bazar-frontend-dev (running)

---

## ⚠️ Проблема: Backend на production не отвечает

### Возможные причины:
1. ❌ Контейнеры не запущены на сервере
2. ❌ БД пустая или не подключена
3. ❌ Неправильные переменные окружения
4. ❌ Не применены миграции Alembic
5. ❌ Firewall блокирует порты

---

## 🔧 План исправления

### Шаг 1: Подключиться к серверу и проверить статус

```bash
# Подключение
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

# Проверить контейнеры
docker ps -a

# Проверить логи
docker logs edu-na-bazar-backend-1 --tail=50
docker logs edu-na-bazar-postgres-1 --tail=50
```

### Шаг 2: Проверить .env файл на сервере

```bash
cd /opt/edu-na-bazar
cat .env

# Должны быть настроены:
# - POSTGRES_PASSWORD (сильный пароль)
# - SECRET_KEY (32+ символов)
# - ALLOWED_ORIGINS (http://176.99.5.211)
# - REACT_APP_API_URL (http://176.99.5.211:8000)
```

### Шаг 3: Создать .env если его нет

```bash
cd /opt/edu-na-bazar

# Создать из примера
cp .env.example .env

# Отредактировать
nano .env
```

**Минимальная конфигурация для .env:**
```env
ENVIRONMENT=production

# Database
POSTGRES_DB=edu_na_bazar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=СГЕНЕРИРОВАТЬ_НИЖЕ

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=СГЕНЕРИРОВАТЬ_НИЖЕ

# CORS
ALLOWED_ORIGINS=http://176.99.5.211,http://localhost

# SMS (отключено)
SMS_ENABLED=false

# API URL
REACT_APP_API_URL=http://176.99.5.211:8000
```

**Генерация паролей:**
```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# POSTGRES_PASSWORD
openssl rand -base64 24
```

### Шаг 4: Перезапустить контейнеры

```bash
cd /opt/edu-na-bazar

# Остановить
docker-compose down

# Запустить с новыми настройками
docker-compose up -d --build

# Проверить статус
docker-compose ps

# Ждем 30 секунд пока БД запустится
sleep 30
```

### Шаг 5: Применить миграции Alembic

```bash
# Проверить текущую версию
docker-compose exec backend alembic current

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить что применилось
docker-compose exec backend alembic current
# Должно показать: 8828a8665651 (head)
```

### Шаг 6: Проверить БД

```bash
# Подключиться к PostgreSQL
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar

# Проверить таблицы
\dt market.*

# Проверить данные
SELECT COUNT(*) FROM market.products;
SELECT COUNT(*) FROM market.categories;
SELECT COUNT(*) FROM market.stores;

# Выйти
\q
```

### Шаг 7: Если БД пустая - загрузить данные

**На локальной машине:**
```powershell
# Создать дамп
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > edu_na_bazar_dump.sql

# Загрузить на сервер
scp edu_na_bazar_dump.sql root@176.99.5.211:/tmp/
# Пароль: sIAS6APDsKh0bL
```

**На сервере:**
```bash
# Восстановить дамп
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/edu_na_bazar_dump.sql

# Проверить
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.products"
```

### Шаг 8: Проверить работу API

```bash
# Health check
curl http://localhost:8000/health
# Должно вернуть: {"status":"ok"}

# Категории
curl http://localhost:8000/api/categories/
# Должно вернуть JSON с категориями

# Товары
curl http://localhost:8000/api/products/?limit=5
# Должно вернуть JSON с товарами
```

### Шаг 9: Проверить firewall

```bash
# Проверить статус UFW
ufw status

# Если порты закрыты - открыть
ufw allow 8000/tcp
ufw allow 3000/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Перезагрузить
ufw reload
```

### Шаг 10: Проверить из браузера

Открыть в браузере:
1. http://176.99.5.211:8000/health
2. http://176.99.5.211:8000/api/categories/
3. http://176.99.5.211:8000/docs (API документация)
4. http://176.99.5.211 (Frontend)

---

## 🐛 Диагностика проблем

### Контейнеры не запускаются

```bash
# Посмотреть логи
docker-compose logs backend
docker-compose logs postgres

# Пересобрать образы
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### БД не подключается

```bash
# Проверить что PostgreSQL запущен
docker exec edu-na-bazar-postgres-1 pg_isready -U postgres

# Проверить переменные окружения
docker exec edu-na-bazar-backend-1 env | grep DATABASE

# Проверить сеть
docker network ls
docker network inspect edu-na-bazar_app-network
```

### API возвращает 500 ошибку

```bash
# Смотреть логи в реальном времени
docker-compose logs -f backend

# Проверить подключение к БД из backend
docker exec -it edu-na-bazar-backend-1 python -c "
from database import engine
import asyncio
async def test():
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('DB OK:', result.scalar())
asyncio.run(test())
"
```

### Frontend не подключается к backend

```bash
# Проверить CORS в backend
docker exec edu-na-bazar-backend-1 cat /app/config.py | grep ALLOWED_ORIGINS

# Должно быть:
# ALLOWED_ORIGINS=http://176.99.5.211,http://localhost

# Проверить API URL в frontend
docker exec edu-na-bazar-frontend-1 cat /usr/share/nginx/html/assets/*.js | grep -o "http://[^\"]*:8000" | head -1

# Должно быть:
# http://176.99.5.211:8000
```

---

## 📊 Чек-лист готовности

### Критично (должно быть ДО запуска)
- [ ] .env файл создан и заполнен
- [ ] SECRET_KEY сгенерирован (32+ символа)
- [ ] POSTGRES_PASSWORD установлен
- [ ] Контейнеры запущены (docker ps)
- [ ] Миграции Alembic применены
- [ ] БД содержит данные
- [ ] Health endpoint отвечает
- [ ] API endpoints работают
- [ ] Firewall настроен

### Важно (в первую неделю)
- [ ] Изображения загружены (uploads/)
- [ ] Backup БД настроен
- [ ] Мониторинг настроен (UptimeRobot)
- [ ] SSL сертификаты (если есть домен)
- [ ] Логирование настроено

### Желательно (в первый месяц)
- [ ] Rate limiting
- [ ] Кэширование Redis
- [ ] CDN для статики
- [ ] Unit тесты
- [ ] E2E тесты

---

## 🚀 Быстрый старт (если все упало)

```bash
# 1. Подключиться
ssh root@176.99.5.211

# 2. Перейти в проект
cd /opt/edu-na-bazar

# 3. Остановить все
docker-compose down

# 4. Проверить .env
cat .env

# 5. Запустить заново
docker-compose up -d --build

# 6. Подождать 30 секунд
sleep 30

# 7. Применить миграции
docker-compose exec backend alembic upgrade head

# 8. Проверить
curl http://localhost:8000/health
docker-compose ps
docker-compose logs -f backend
```

---

## 📞 Полезные команды

```bash
# Перезапуск всех сервисов
docker-compose restart

# Перезапуск только backend
docker-compose restart backend

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f postgres

# Проверка ресурсов
docker stats

# Очистка (ОСТОРОЖНО!)
docker-compose down -v  # Удалит volumes с данными!

# Backup БД
docker exec edu-na-bazar-postgres-1 pg_dump -U postgres edu_na_bazar > backup_$(date +%Y%m%d).sql
```

---

## ✅ Критерии успеха

Деплой считается успешным когда:

1. ✅ `docker ps` показывает 4 запущенных контейнера
2. ✅ `curl http://localhost:8000/health` возвращает `{"status":"ok"}`
3. ✅ `curl http://localhost:8000/api/categories/` возвращает JSON с категориями
4. ✅ http://176.99.5.211:8000/health открывается в браузере
5. ✅ http://176.99.5.211 показывает frontend
6. ✅ В браузере нет ошибок CORS в консоли
7. ✅ Категории и товары загружаются на главной странице

---

**Создано**: 25.11.2025, 18:15  
**Статус**: Backend локально работает, нужно проверить production сервер  
**Следующий шаг**: Подключиться к серверу и выполнить диагностику
