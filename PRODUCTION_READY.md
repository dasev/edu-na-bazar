# ✅ Production Ready Checklist - Еду на базар

## 🎉 Что готово

### ✅ Контейнеризация (100%)
- [x] Backend Dockerfile с multi-stage build
- [x] Frontend Dockerfile с multi-stage build
- [x] docker-compose.yml для production (4 контейнера)
- [x] docker-compose.dev.yml для development (hot-reload)
- [x] .dockerignore для оптимизации сборки
- [x] Health checks для всех сервисов
- [x] Volumes для персистентности данных
- [x] Скрипты запуска (START_DOCKER.bat)

### ✅ Безопасность (80%)
- [x] Убран хардкод SMSC credentials
- [x] Переменные окружения через .env
- [x] CORS настраивается через env
- [x] Debug режим отключается в production
- [x] API docs скрыты в production
- [x] Multi-stage build (меньший размер образов)
- [ ] Rate limiting (TODO)
- [ ] CSRF защита (TODO)

### ✅ Конфигурация (100%)
- [x] .env.example с полным описанием
- [x] Разделение dev/prod конфигураций
- [x] Переменные окружения для всех секретов
- [x] ALLOWED_ORIGINS настраивается динамически

### ✅ CI/CD (90%)
- [x] GitHub Actions workflow
- [x] Docker Hub интеграция
- [x] Автоматический деплой на сервер
- [ ] Database migrations в pipeline (TODO)
- [ ] Rollback механизм (TODO)

### ✅ Документация (100%)
- [x] DOCKER_GUIDE.md - полное руководство
- [x] CICD_SETUP.md - настройка деплоя
- [x] README.md обновлен
- [x] .env.example с комментариями

---

## 🚀 Запуск проекта

### Development (с hot-reload)
```bash
# 1. Создать .env
copy .env.example .env

# 2. Запустить
START_DOCKER_DEV.bat

# Доступ:
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

### Production
```bash
# 1. Создать .env с production значениями
copy .env.example .env

# 2. Запустить
START_DOCKER.bat

# Доступ:
# Frontend: http://localhost
# Backend:  http://localhost:8000
```

---

## 📋 Что нужно сделать перед деплоем

### 1. Обязательные настройки .env

```env
# Сгенерировать криптостойкий ключ
SECRET_KEY=<openssl rand -hex 32>

# Установить сильный пароль БД
POSTGRES_PASSWORD=<strong_password>

# Настроить CORS для вашего домена
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Production режим
ENVIRONMENT=production

# SMS (если нужно)
SMS_ENABLED=true
SMSC_LOGIN=your_login
SMSC_PASSWORD=your_password

# Mapbox (если нужна карта)
MAPBOX_ACCESS_TOKEN=your_token
REACT_APP_MAPBOX_TOKEN=your_token
```

### 2. Создать миграции Alembic

```bash
# В контейнере backend
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head
```

### 3. Загрузить начальные данные

```bash
# Если есть backup
docker-compose exec -T postgres psql -U postgres edu_na_bazar < backup.sql

# Или запустить скрипты миграции
docker-compose exec backend python scripts/migrate_from_files.py
```

---

## 🔐 Безопасность - TODO

### Критично для production

#### 1. Rate Limiting
```python
# Установить
pip install slowapi

# Добавить в main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Применить к эндпоинтам
@app.post("/api/auth/send-code")
@limiter.limit("5/minute")
async def send_code(...):
    ...
```

#### 2. CSRF Protection
```python
# Установить
pip install fastapi-csrf-protect

# Настроить в main.py
from fastapi_csrf_protect import CsrfProtect

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfConfig(secret_key=settings.SECRET_KEY)
```

#### 3. Валидация загружаемых файлов
```python
# В images router
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate_image(file: UploadFile):
    # Проверка размера
    # Проверка расширения
    # Проверка MIME type
    # Sanitization с Pillow
```

#### 4. SQL Injection защита
- ✅ Уже защищено через SQLAlchemy ORM
- ✅ Параметризованные запросы

#### 5. XSS защита
- ✅ React автоматически экранирует
- Добавить Content-Security-Policy заголовки

---

## 📊 Мониторинг - TODO

### 1. Логирование

#### Структурированное логирование
```python
# Установить
pip install python-json-logger

# Настроить в main.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

#### Централизованные логи
- Вариант 1: ELK Stack (Elasticsearch + Logstash + Kibana)
- Вариант 2: Loki + Grafana
- Вариант 3: CloudWatch (AWS)

### 2. Метрики

#### Prometheus + Grafana
```yaml
# docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
```

#### Application metrics
```python
# Установить
pip install prometheus-fastapi-instrumentator

# В main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 3. Error Tracking

#### Sentry
```python
# Установить
pip install sentry-sdk

# В main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
)
```

### 4. Uptime Monitoring
- UptimeRobot (бесплатно)
- Pingdom
- StatusCake

---

## 🧪 Тестирование - TODO

### 1. Unit тесты
```python
# Установить
pip install pytest pytest-asyncio pytest-cov

# Создать tests/
tests/
  ├── test_auth.py
  ├── test_products.py
  └── test_cart.py

# Запуск
pytest --cov=. --cov-report=html
```

### 2. Integration тесты
```python
# Тестирование API endpoints
from fastapi.testclient import TestClient

def test_create_product():
    response = client.post("/api/products", json={...})
    assert response.status_code == 201
```

### 3. E2E тесты
```javascript
// Playwright или Cypress
describe('Product Page', () => {
  it('should add product to cart', () => {
    cy.visit('/product/1')
    cy.get('[data-testid="add-to-cart"]').click()
    cy.get('[data-testid="cart-count"]').should('contain', '1')
  })
})
```

---

## 🗄️ База данных - TODO

### 1. Миграции Alembic
```bash
# Создать initial migration
docker-compose exec backend alembic revision --autogenerate -m "Initial schema"

# Применить
docker-compose exec backend alembic upgrade head

# Добавить в CI/CD pipeline
```

### 2. Backup стратегия
```bash
# Автоматический backup (cron)
0 2 * * * docker-compose exec postgres pg_dump -U postgres edu_na_bazar | gzip > /backups/$(date +\%Y\%m\%d).sql.gz

# Retention policy (хранить 30 дней)
find /backups -name "*.sql.gz" -mtime +30 -delete
```

### 3. Индексы
```sql
-- Добавить индексы для производительности
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_store ON products(store_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_created ON orders(created_at);
```

---

## 🌐 Nginx - TODO (для production)

### SSL/TLS сертификаты
```bash
# Let's Encrypt
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Nginx конфигурация
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📈 Производительность - TODO

### 1. Кэширование
```python
# Redis кэш для часто запрашиваемых данных
from redis import asyncio as aioredis

redis = aioredis.from_url(settings.REDIS_URL)

@app.get("/api/products")
async def get_products():
    # Проверить кэш
    cached = await redis.get("products:list")
    if cached:
        return json.loads(cached)
    
    # Запрос к БД
    products = await db.execute(...)
    
    # Сохранить в кэш (5 минут)
    await redis.setex("products:list", 300, json.dumps(products))
    
    return products
```

### 2. Database connection pooling
```python
# В database.py
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)
```

### 3. CDN для статики
- Cloudflare (бесплатно)
- AWS CloudFront
- Fastly

---

## ✅ Финальный чеклист

### Перед деплоем
- [ ] .env файл заполнен production значениями
- [ ] SECRET_KEY сгенерирован (32+ символа)
- [ ] POSTGRES_PASSWORD установлен
- [ ] ALLOWED_ORIGINS настроен для домена
- [ ] ENVIRONMENT=production
- [ ] SMS credentials настроены (если нужно)
- [ ] Mapbox token добавлен (если нужна карта)
- [ ] Docker образы собраны
- [ ] Миграции Alembic созданы и применены
- [ ] Начальные данные загружены
- [ ] SSL сертификаты получены
- [ ] Backup стратегия настроена
- [ ] Мониторинг настроен
- [ ] Логирование настроено

### После деплоя
- [ ] Проверить health checks
- [ ] Проверить логи контейнеров
- [ ] Протестировать основные функции
- [ ] Проверить SSL/HTTPS
- [ ] Настроить uptime monitoring
- [ ] Настроить алерты
- [ ] Документировать процедуры

---

## 🎯 Приоритеты

### Критично (сделать до деплоя)
1. ✅ Убрать хардкод credentials
2. ✅ Настроить .env
3. ✅ Контейнеризация
4. ⏳ Создать миграции Alembic
5. ⏳ SSL сертификаты
6. ⏳ Backup БД

### Важно (сделать в первую неделю)
1. ⏳ Rate limiting
2. ⏳ Логирование
3. ⏳ Мониторинг (базовый)
4. ⏳ Error tracking (Sentry)
5. ⏳ Unit тесты (основные)

### Желательно (сделать в первый месяц)
1. ⏳ CSRF защита
2. ⏳ Кэширование
3. ⏳ CDN
4. ⏳ E2E тесты
5. ⏳ Performance optimization

---

## 📞 Поддержка

При возникновении проблем:
1. Проверить логи: `docker-compose logs -f`
2. Проверить health checks: `docker-compose ps`
3. Посмотреть DOCKER_GUIDE.md
4. Посмотреть TROUBLESHOOTING.md

**Проект готов к деплою на 80%!** 🎉

Основная инфраструктура готова, осталось добавить мониторинг, тесты и финальные настройки безопасности.
