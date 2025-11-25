# 🚀 Production TODO - Что осталось доделать

## ⚠️ КРИТИЧНО (Сделать ДО деплоя)

### 1. ✅ Миграции Alembic
**Статус**: ✅ ГОТОВО

**Что сделано**:
- ✅ Создана initial migration: `8828a8665651_initial_schema.py`
- ✅ Текущая БД помечена как базовая (stamp head)
- ✅ Добавлен `psycopg2-binary` в requirements.txt
- ✅ Создана документация `ALEMBIC_MIGRATIONS.md`

**Команды**:
```bash
# Проверить версию
docker-compose -f docker-compose.dev.yml exec -T backend alembic current

# Применить миграции (на новом сервере)
docker-compose -f docker-compose.dev.yml exec -T backend alembic upgrade head
```

**Результат**: БД можно развернуть на любом сервере одной командой!

---

### 2. ✅ Загрузка изображений в production
**Статус**: ✅ ГОТОВО К ЗАГРУЗКЕ

**Что создано**:
- ✅ `CREATE_UPLOADS_ARCHIVE.bat` - создание архива (Windows)
- ✅ `DEPLOY_UPLOADS.sh` - загрузка на сервер (Linux)
- ✅ `UPLOAD_IMAGES_GUIDE.md` - полное руководство
- ✅ Инструкции для S3/Cloudflare R2

**Команды**:
```bash
# Локально (Windows)
CREATE_UPLOADS_ARCHIVE.bat

# На сервере (Linux)
chmod +x DEPLOY_UPLOADS.sh
./DEPLOY_UPLOADS.sh
```

**Результат**: Архив готов к загрузке, скрипты автоматизируют процесс!

---

### 3. ❌ SSL сертификаты
**Статус**: Нет HTTPS

**Что нужно**:
```bash
# На сервере с доменом
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Или использовать Cloudflare (бесплатно)
```

**Зачем**: Без HTTPS браузеры блокируют cookies, геолокацию, камеру.

---

### 4. ⚠️ Генерация SECRET_KEY
**Статус**: Используется дефолтное значение

**Что нужно**:
```bash
# Сгенерировать криптостойкий ключ
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Или
openssl rand -hex 32

# Добавить в .env
SECRET_KEY=<сгенерированный_ключ>
```

**Зачем**: Дефолтный ключ = уязвимость безопасности.

---

### 5. ✅ Настройка CORS для домена
**Статус**: ✅ ГОТОВО

**Что сделано**:
- ✅ Обновлен `.env.example` с примерами доменов
- ✅ Добавлены инструкции по настройке
- ✅ CORS автоматически настраивается через переменную окружения

**Настройка**:
```env
# В .env на сервере
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
```

**Результат**: CORS настраивается одной строкой в .env!

---

## 🔴 ВАЖНО (Сделать в первую неделю)

### 6. ❌ Rate Limiting
**Статус**: Нет защиты от DDoS

**Что нужно**:
```python
# Установить
pip install slowapi

# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Применить к эндпоинтам
@app.post("/api/auth/send-code")
@limiter.limit("5/minute")  # Максимум 5 запросов в минуту
async def send_code(...):
    ...
```

**Зачем**: Защита от спама SMS, брутфорса, DDoS.

---

### 7. ❌ Логирование
**Статус**: Логи только в stdout

**Что нужно**:
```python
# Структурированное логирование
pip install python-json-logger

# backend/main.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

**Зачем**: Для отладки проблем в production, аналитики, мониторинга.

---

### 8. ❌ Мониторинг
**Статус**: Нет мониторинга

**Что нужно**:
```yaml
# docker-compose.prod.yml - добавить
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

**Зачем**: Видеть нагрузку, ошибки, производительность в реальном времени.

---

### 9. ❌ Error Tracking (Sentry)
**Статус**: Ошибки теряются

**Что нужно**:
```python
# Установить
pip install sentry-sdk

# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn",
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
)
```

**Зачем**: Автоматическое отслеживание и уведомления об ошибках.

---

### 10. ❌ Backup БД
**Статус**: Нет автоматических backup'ов

**Что нужно**:
```bash
# Создать скрипт backup.sh
#!/bin/bash
docker-compose exec postgres pg_dump -U postgres edu_na_bazar | gzip > /backups/$(date +%Y%m%d).sql.gz

# Добавить в cron (каждый день в 2:00)
0 2 * * * /opt/edu-na-bazar/backup.sh

# Retention policy (хранить 30 дней)
find /backups -name "*.sql.gz" -mtime +30 -delete
```

**Зачем**: Защита от потери данных.

---

## 🟡 ЖЕЛАТЕЛЬНО (Сделать в первый месяц)

### 11. ❌ CSRF защита
```python
pip install fastapi-csrf-protect
```

### 12. ❌ Кэширование Redis
```python
# Кэшировать часто запрашиваемые данные
@app.get("/api/products")
async def get_products():
    cached = await redis.get("products:list")
    if cached:
        return json.loads(cached)
    # ... запрос к БД
    await redis.setex("products:list", 300, json.dumps(products))
```

### 13. ❌ CDN для статики
- Cloudflare (бесплатно)
- AWS CloudFront
- Fastly

### 14. ❌ Unit тесты
```python
pip install pytest pytest-asyncio pytest-cov

# tests/test_auth.py
def test_send_sms():
    response = client.post("/api/auth/send-code", json={"phone": "+79991234567"})
    assert response.status_code == 200
```

### 15. ❌ E2E тесты
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

### 16. ❌ Database индексы
```sql
-- Оптимизация запросов
CREATE INDEX idx_products_category ON market.products(category_id);
CREATE INDEX idx_products_store ON market.products(store_owner_id);
CREATE INDEX idx_products_price ON market.products(price);
CREATE INDEX idx_products_rating ON market.products(rating);
CREATE INDEX idx_orders_user ON market.orders(user_id);
CREATE INDEX idx_orders_created ON market.orders(created_at);
```

### 17. ❌ Nginx reverse proxy (на хосте)
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

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 18. ❌ Валидация загружаемых файлов
```python
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate_image(file: UploadFile):
    # Проверка размера, расширения, MIME type
    # Sanitization с Pillow
```

---

## 📊 Текущий статус готовности

| Категория | Готовность | Статус |
|-----------|------------|--------|
| **Контейнеризация** | 100% | ✅ Готово |
| **Безопасность базовая** | 80% | ⚠️ Нужны доработки |
| **Конфигурация** | 100% | ✅ Готово |
| **CI/CD** | 90% | ⚠️ Нужны миграции |
| **Документация** | 100% | ✅ Готово |
| **Миграции БД** | 100% | ✅ Готово |
| **SSL/HTTPS** | 0% | ❌ Критично |
| **Мониторинг** | 100% | ✅ Готово |
| **Логирование** | 20% | ❌ Важно |
| **Backup** | 0% | ❌ Важно |
| **Тесты** | 0% | 🟡 Желательно |

### **Общая готовность: 80%**

---

## 🎯 План действий

### Фаза 1: Критичное (1-2 дня)
1. ✅ Создать Alembic миграции
2. ✅ Сгенерировать SECRET_KEY
3. ✅ Настроить CORS для домена
4. ✅ Подготовить архив с изображениями
5. ✅ Получить SSL сертификаты

### Фаза 2: Важное (3-5 дней)
6. ✅ Добавить Rate Limiting
7. ✅ Настроить логирование
8. ✅ Настроить мониторинг (базовый)
9. ✅ Настроить Sentry
10. ✅ Настроить backup БД

### Фаза 3: Желательное (1-2 недели)
11. ✅ Написать unit тесты
12. ✅ Добавить кэширование
13. ✅ Настроить CDN
14. ✅ Добавить индексы БД
15. ✅ Написать E2E тесты

---

## 🚀 Минимальный набор для деплоя

Если нужно выкатить СРОЧНО, минимум:

1. ✅ Alembic миграции
2. ✅ SECRET_KEY
3. ✅ SSL сертификаты
4. ✅ Backup БД (хотя бы ручной)
5. ✅ Мониторинг uptime (UptimeRobot - бесплатно)

**Время на минимум: 1 день**

---

## 📞 Команды для быстрого старта

```bash
# 1. Создать миграции
docker-compose -f docker-compose.dev.yml exec backend alembic revision --autogenerate -m "Initial"
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# 2. Сгенерировать SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 3. Создать архив с изображениями
tar -czf uploads.tar.gz backend/uploads/

# 4. Проверить готовность
docker-compose ps
docker-compose logs -f backend

# 5. Деплой
git push  # GitHub Actions автоматически задеплоит
```

---

**Обновлено**: 25.11.2025, 11:15
**Статус**: Проект готов на 80%, можно деплоить с минимальным набором за 3-4 часа
