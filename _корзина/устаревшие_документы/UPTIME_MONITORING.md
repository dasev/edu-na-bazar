# 📊 Uptime Monitoring - Мониторинг доступности

## 🎯 Цель

Отслеживать доступность сервисов 24/7 и получать уведомления при сбоях.

---

## 🆓 Вариант 1: UptimeRobot (Рекомендуется для старта)

**Бесплатно:** 50 мониторов, проверка каждые 5 минут

### Настройка:

1. **Регистрация:**
   - Перейти на https://uptimerobot.com
   - Создать аккаунт (бесплатно)

2. **Добавить мониторы:**

   **Frontend Monitor:**
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Еду на базар - Frontend`
   - URL: `https://yourdomain.com`
   - Monitoring Interval: `5 minutes`
   - Monitor Timeout: `30 seconds`
   - Alert Contacts: ваш email/Telegram

   **Backend API Monitor:**
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Еду на базар - API Health`
   - URL: `https://yourdomain.com/api/health`
   - Monitoring Interval: `5 minutes`
   - Keyword: `"status":"ok"` (проверка содержимого ответа)

   **Database Monitor (через API):**
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Еду на базар - Database`
   - URL: `https://yourdomain.com/api/categories`
   - Monitoring Interval: `5 minutes`

3. **Настроить уведомления:**
   - Email (бесплатно)
   - Telegram (через бота)
   - Webhook (для интеграции)
   - SMS (платно)

4. **Public Status Page:**
   - Создать публичную страницу статуса
   - URL: `https://stats.uptimerobot.com/your-page`
   - Показывать uptime за 30/60/90 дней

### Преимущества:
- ✅ Бесплатно до 50 мониторов
- ✅ Простая настройка (5 минут)
- ✅ Email/Telegram уведомления
- ✅ Публичная страница статуса
- ✅ История за 6 месяцев
- ✅ API для интеграции

---

## 🔧 Вариант 2: Uptime Kuma (Self-hosted)

**Бесплатно:** Полностью, но нужен свой сервер

### Установка через Docker:

```bash
# Создать docker-compose.monitoring.yml
cat > docker-compose.monitoring.yml << 'EOF'
version: '3.8'

services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    volumes:
      - uptime-kuma-data:/app/data
    ports:
      - "3001:3001"
    restart: unless-stopped
    networks:
      - monitoring

volumes:
  uptime-kuma-data:

networks:
  monitoring:
    driver: bridge
EOF

# Запустить
docker-compose -f docker-compose.monitoring.yml up -d

# Открыть в браузере
# http://your_server_ip:3001
```

### Настройка:

1. **Первый запуск:**
   - Создать admin аккаунт
   - Установить пароль

2. **Добавить мониторы:**
   - Frontend: `https://yourdomain.com`
   - API Health: `https://yourdomain.com/api/health`
   - Database: `https://yourdomain.com/api/categories`
   - PostgreSQL: `postgres://localhost:5432` (внутренний)
   - Redis: `redis://localhost:6379` (внутренний)

3. **Настроить уведомления:**
   - Telegram Bot
   - Discord Webhook
   - Email (SMTP)
   - Slack
   - 90+ интеграций

4. **Status Page:**
   - Создать публичную страницу
   - Настроить домен (опционально)

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Красивый UI
- ✅ Множество интеграций
- ✅ Мониторинг внутренних сервисов
- ✅ Графики и статистика
- ✅ Unlimited мониторы

### Недостатки:
- ❌ Нужен отдельный сервер
- ❌ Нужно настраивать самому

---

## 📱 Вариант 3: Telegram Bot (Простой)

Создам простой скрипт для мониторинга через Telegram.

### Установка:

```bash
# На сервере создать скрипт
cat > /opt/uptime-monitor.sh << 'EOF'
#!/bin/bash

# Telegram Bot настройки
BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# URL для проверки
FRONTEND_URL="https://yourdomain.com"
API_URL="https://yourdomain.com/api/health"

# Функция отправки в Telegram
send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${message}" \
        -d parse_mode="HTML" > /dev/null
}

# Проверка Frontend
if ! curl -s -f -o /dev/null -w "%{http_code}" "${FRONTEND_URL}" | grep -q "200"; then
    send_telegram "🔴 <b>ALERT:</b> Frontend недоступен! ${FRONTEND_URL}"
fi

# Проверка API
if ! curl -s -f "${API_URL}" | grep -q "ok"; then
    send_telegram "🔴 <b>ALERT:</b> API недоступен! ${API_URL}"
fi

# Проверка контейнеров
if ! docker ps | grep -q "edu-na-bazar-backend"; then
    send_telegram "🔴 <b>ALERT:</b> Backend контейнер не запущен!"
fi

if ! docker ps | grep -q "edu-na-bazar-frontend"; then
    send_telegram "🔴 <b>ALERT:</b> Frontend контейнер не запущен!"
fi

# Проверка места на диске
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    send_telegram "⚠️ <b>WARNING:</b> Диск заполнен на ${DISK_USAGE}%"
fi

# Проверка памяти
MEM_USAGE=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
if [ "$MEM_USAGE" -gt 90 ]; then
    send_telegram "⚠️ <b>WARNING:</b> Память заполнена на ${MEM_USAGE}%"
fi
EOF

# Сделать исполняемым
chmod +x /opt/uptime-monitor.sh

# Добавить в cron (каждые 5 минут)
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/uptime-monitor.sh") | crontab -
```

### Создание Telegram бота:

1. Открыть [@BotFather](https://t.me/BotFather)
2. Отправить `/newbot`
3. Указать имя: `Еду на базар Monitor`
4. Указать username: `edunabazar_monitor_bot`
5. Получить `BOT_TOKEN`
6. Получить `CHAT_ID`:
   ```bash
   # Отправить сообщение боту, затем:
   curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   # Найти "chat":{"id":123456789}
   ```

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Мгновенные уведомления
- ✅ Простая настройка
- ✅ Мониторинг ресурсов сервера

---

## 🌐 Вариант 4: Healthchecks.io

**Бесплатно:** 20 проверок, интервал 1 минута

### Настройка:

1. Регистрация на https://healthchecks.io
2. Создать проверки:
   - Frontend
   - API
   - Scheduled tasks (если есть)
3. Настроить уведомления (Email, Telegram, Slack)

### Интеграция с cron:

```bash
# Добавить в конец cron задач
*/5 * * * * curl -fsS -m 10 --retry 5 https://hc-ping.com/YOUR-UUID-HERE > /dev/null
```

---

## 📊 Вариант 5: Prometheus + Grafana (Продвинутый)

Для полного мониторинга метрик.

### Установка:

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "3002:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
```

### prometheus.yml:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  # Backend API
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  # Node Exporter (системные метрики)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # cAdvisor (Docker метрики)
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

### Добавить метрики в FastAPI:

```python
# backend/requirements.txt
prometheus-fastapi-instrumentator==6.1.0

# backend/main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(...)

# Добавить метрики
Instrumentator().instrument(app).expose(app)
```

---

## 📋 Сравнение вариантов

| Вариант | Сложность | Стоимость | Функции | Рекомендация |
|---------|-----------|-----------|---------|--------------|
| **UptimeRobot** | ⭐ Легко | 💰 Бесплатно | ⭐⭐⭐ Базовые | ✅ Для старта |
| **Uptime Kuma** | ⭐⭐ Средне | 💰 Бесплатно | ⭐⭐⭐⭐ Хорошие | ✅ Self-hosted |
| **Telegram Bot** | ⭐ Легко | 💰 Бесплатно | ⭐⭐ Простые | ✅ Быстрый старт |
| **Healthchecks.io** | ⭐ Легко | 💰 Бесплатно | ⭐⭐⭐ Базовые | ✅ Для cron |
| **Prometheus** | ⭐⭐⭐ Сложно | 💰 Бесплатно | ⭐⭐⭐⭐⭐ Полные | ⚠️ Для роста |

---

## 🚀 Рекомендуемая стратегия

### Этап 1: Минимум (День 1)
1. ✅ UptimeRobot - внешний мониторинг
2. ✅ Telegram Bot - уведомления

### Этап 2: Улучшение (Неделя 1)
3. ✅ Uptime Kuma - детальный мониторинг
4. ✅ Healthchecks.io - для cron задач

### Этап 3: Продвинутый (Месяц 1)
5. ✅ Prometheus + Grafana - метрики и дашборды

---

## 📝 Быстрый старт (5 минут)

### 1. UptimeRobot

```bash
# 1. Зарегистрироваться на uptimerobot.com
# 2. Добавить мониторы:
#    - https://yourdomain.com (Frontend)
#    - https://yourdomain.com/api/health (API)
# 3. Настроить email уведомления
# 4. Готово!
```

### 2. Telegram Bot

```bash
# 1. Создать бота через @BotFather
# 2. Получить BOT_TOKEN и CHAT_ID
# 3. Скопировать скрипт на сервер
# 4. Настроить cron
# 5. Готово!
```

---

## ✅ Checklist

- [ ] Выбран сервис мониторинга
- [ ] Добавлены мониторы для Frontend
- [ ] Добавлены мониторы для API
- [ ] Настроены уведомления (Email/Telegram)
- [ ] Создана публичная страница статуса (опционально)
- [ ] Протестированы уведомления
- [ ] Настроен мониторинг ресурсов сервера
- [ ] Добавлен мониторинг БД (опционально)

---

## 🔍 Что мониторить

### Обязательно:
- ✅ Frontend доступность (HTTP 200)
- ✅ API Health endpoint (`/api/health`)
- ✅ Время отклика (< 2 секунды)

### Желательно:
- ✅ Database доступность (через API)
- ✅ Место на диске (< 80%)
- ✅ Использование памяти (< 90%)
- ✅ CPU usage (< 80%)
- ✅ Docker контейнеры (running)

### Опционально:
- ✅ SSL сертификат (срок действия)
- ✅ Время ответа БД
- ✅ Размер логов
- ✅ Количество ошибок в логах

---

## 📞 Контакты для уведомлений

Настройте несколько каналов:
1. **Email** - основной (всегда)
2. **Telegram** - мгновенный (критичные)
3. **SMS** - критичные (платно)
4. **Webhook** - для интеграции с другими системами

---

**Создано**: 25.11.2025  
**Рекомендация**: Начните с UptimeRobot + Telegram Bot (настройка 10 минут)
