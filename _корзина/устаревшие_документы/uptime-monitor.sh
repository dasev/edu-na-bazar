#!/bin/bash

#############################################
# Uptime Monitor для "Еду на базар"
# Мониторинг доступности и уведомления в Telegram
#############################################

# ========== НАСТРОЙКИ ==========
# Получить BOT_TOKEN: https://t.me/BotFather
BOT_TOKEN="YOUR_BOT_TOKEN_HERE"

# Получить CHAT_ID: отправить сообщение боту, затем:
# curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
CHAT_ID="YOUR_CHAT_ID_HERE"

# URL для проверки
FRONTEND_URL="https://yourdomain.com"
API_HEALTH_URL="https://yourdomain.com/api/health"
API_CATEGORIES_URL="https://yourdomain.com/api/categories"

# Пороги для предупреждений
DISK_THRESHOLD=80      # % заполнения диска
MEMORY_THRESHOLD=90    # % использования памяти
CPU_THRESHOLD=80       # % использования CPU

# Файл для хранения состояния (чтобы не спамить)
STATE_FILE="/tmp/uptime-monitor-state.txt"

# ========== ФУНКЦИИ ==========

# Отправка сообщения в Telegram
send_telegram() {
    local message="$1"
    local emoji="$2"
    
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${emoji} ${message}" \
        -d parse_mode="HTML" > /dev/null 2>&1
}

# Проверка изменения состояния (чтобы не спамить)
check_state_change() {
    local key="$1"
    local new_state="$2"
    
    if [ ! -f "$STATE_FILE" ]; then
        touch "$STATE_FILE"
    fi
    
    local old_state=$(grep "^${key}=" "$STATE_FILE" 2>/dev/null | cut -d'=' -f2)
    
    if [ "$old_state" != "$new_state" ]; then
        # Состояние изменилось
        sed -i "/^${key}=/d" "$STATE_FILE" 2>/dev/null
        echo "${key}=${new_state}" >> "$STATE_FILE"
        return 0  # Изменилось
    fi
    
    return 1  # Не изменилось
}

# ========== ПРОВЕРКИ ==========

echo "🔍 Запуск проверок..."

# 1. Проверка Frontend
echo "Проверка Frontend: $FRONTEND_URL"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "${FRONTEND_URL}" 2>/dev/null)

if [ "$HTTP_CODE" != "200" ]; then
    if check_state_change "frontend" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> Frontend недоступен!
        
URL: ${FRONTEND_URL}
HTTP Code: ${HTTP_CODE}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "🔴"
    fi
else
    if check_state_change "frontend" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> Frontend снова доступен!
        
URL: ${FRONTEND_URL}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ Frontend OK (HTTP $HTTP_CODE)"
fi

# 2. Проверка API Health
echo "Проверка API Health: $API_HEALTH_URL"
API_RESPONSE=$(curl -s -m 10 "${API_HEALTH_URL}" 2>/dev/null)

if ! echo "$API_RESPONSE" | grep -q "ok"; then
    if check_state_change "api_health" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> API Health недоступен!
        
URL: ${API_HEALTH_URL}
Ответ: ${API_RESPONSE:-Нет ответа}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "🔴"
    fi
else
    if check_state_change "api_health" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> API Health снова работает!
        
URL: ${API_HEALTH_URL}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ API Health OK"
fi

# 3. Проверка API Categories (проверка БД)
echo "Проверка API Categories: $API_CATEGORIES_URL"
CATEGORIES_HTTP=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "${API_CATEGORIES_URL}" 2>/dev/null)

if [ "$CATEGORIES_HTTP" != "200" ]; then
    if check_state_change "api_categories" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> API Categories недоступен (возможно проблема с БД)!
        
URL: ${API_CATEGORIES_URL}
HTTP Code: ${CATEGORIES_HTTP}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "🔴"
    fi
else
    if check_state_change "api_categories" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> API Categories снова работает!
        
URL: ${API_CATEGORIES_URL}
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ API Categories OK (HTTP $CATEGORIES_HTTP)"
fi

# 4. Проверка Docker контейнеров
echo "Проверка Docker контейнеров..."

# Backend
if ! docker ps --format '{{.Names}}' | grep -q "edu-na-bazar-backend"; then
    if check_state_change "container_backend" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> Backend контейнер не запущен!
        
Контейнер: edu-na-bazar-backend
Время: $(date '+%Y-%m-%d %H:%M:%S')
        
Команда для перезапуска:
<code>docker-compose up -d backend</code>" "🔴"
    fi
else
    if check_state_change "container_backend" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> Backend контейнер запущен!
        
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ Backend контейнер работает"
fi

# Frontend
if ! docker ps --format '{{.Names}}' | grep -q "edu-na-bazar-frontend"; then
    if check_state_change "container_frontend" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> Frontend контейнер не запущен!
        
Контейнер: edu-na-bazar-frontend
Время: $(date '+%Y-%m-%d %H:%M:%S')
        
Команда для перезапуска:
<code>docker-compose up -d frontend</code>" "🔴"
    fi
else
    if check_state_change "container_frontend" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> Frontend контейнер запущен!
        
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ Frontend контейнер работает"
fi

# PostgreSQL
if ! docker ps --format '{{.Names}}' | grep -q "edu-na-bazar-postgres"; then
    if check_state_change "container_postgres" "down"; then
        send_telegram "<b>🔴 КРИТИЧНО:</b> PostgreSQL контейнер не запущен!
        
Контейнер: edu-na-bazar-postgres
Время: $(date '+%Y-%m-%d %H:%M:%S')
        
Команда для перезапуска:
<code>docker-compose up -d postgres</code>" "🔴"
    fi
else
    if check_state_change "container_postgres" "up"; then
        send_telegram "<b>✅ ВОССТАНОВЛЕНО:</b> PostgreSQL контейнер запущен!
        
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ PostgreSQL контейнер работает"
fi

# 5. Проверка места на диске
echo "Проверка места на диске..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    if check_state_change "disk_usage" "high"; then
        send_telegram "<b>⚠️ ПРЕДУПРЕЖДЕНИЕ:</b> Диск заполнен!
        
Использовано: ${DISK_USAGE}%
Порог: ${DISK_THRESHOLD}%
Время: $(date '+%Y-%m-%d %H:%M:%S')
        
Рекомендации:
- Очистить логи Docker: <code>docker system prune -a</code>
- Проверить большие файлы: <code>du -sh /* | sort -h</code>" "⚠️"
    fi
else
    if check_state_change "disk_usage" "normal"; then
        send_telegram "<b>✅ НОРМА:</b> Использование диска в норме
        
Использовано: ${DISK_USAGE}%
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
    fi
    echo "✅ Диск: ${DISK_USAGE}% (норма)"
fi

# 6. Проверка памяти
echo "Проверка памяти..."
if command -v free &> /dev/null; then
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    
    if [ "$MEM_USAGE" -gt "$MEMORY_THRESHOLD" ]; then
        if check_state_change "memory_usage" "high"; then
            send_telegram "<b>⚠️ ПРЕДУПРЕЖДЕНИЕ:</b> Высокое использование памяти!
            
Использовано: ${MEM_USAGE}%
Порог: ${MEMORY_THRESHOLD}%
Время: $(date '+%Y-%m-%d %H:%M:%S')
            
Рекомендации:
- Проверить процессы: <code>docker stats</code>
- Перезапустить контейнеры: <code>docker-compose restart</code>" "⚠️"
        fi
    else
        if check_state_change "memory_usage" "normal"; then
            send_telegram "<b>✅ НОРМА:</b> Использование памяти в норме
            
Использовано: ${MEM_USAGE}%
Время: $(date '+%Y-%m-%d %H:%M:%S')" "✅"
        fi
        echo "✅ Память: ${MEM_USAGE}% (норма)"
    fi
fi

# 7. Проверка CPU (средняя за 1 минуту)
echo "Проверка CPU..."
if command -v uptime &> /dev/null; then
    CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    CPU_CORES=$(nproc)
    CPU_PERCENT=$(echo "scale=0; ($CPU_LOAD / $CPU_CORES) * 100" | bc 2>/dev/null || echo "0")
    
    if [ "$CPU_PERCENT" -gt "$CPU_THRESHOLD" ]; then
        if check_state_change "cpu_usage" "high"; then
            send_telegram "<b>⚠️ ПРЕДУПРЕЖДЕНИЕ:</b> Высокая нагрузка на CPU!
            
Load Average: ${CPU_LOAD}
Использовано: ~${CPU_PERCENT}%
Ядер: ${CPU_CORES}
Порог: ${CPU_THRESHOLD}%
Время: $(date '+%Y-%m-%d %H:%M:%S')
            
Рекомендации:
- Проверить процессы: <code>top</code>
- Проверить Docker: <code>docker stats</code>" "⚠️"
        fi
    else
        echo "✅ CPU: Load ${CPU_LOAD} (~${CPU_PERCENT}%, норма)"
    fi
fi

# 8. Проверка SSL сертификата (если есть)
echo "Проверка SSL сертификата..."
if [[ "$FRONTEND_URL" == https://* ]]; then
    DOMAIN=$(echo "$FRONTEND_URL" | sed 's|https://||' | sed 's|/.*||')
    SSL_EXPIRY=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    
    if [ -n "$SSL_EXPIRY" ]; then
        SSL_EXPIRY_EPOCH=$(date -d "$SSL_EXPIRY" +%s 2>/dev/null)
        CURRENT_EPOCH=$(date +%s)
        DAYS_LEFT=$(( ($SSL_EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))
        
        if [ "$DAYS_LEFT" -lt 30 ]; then
            if check_state_change "ssl_expiry" "warning"; then
                send_telegram "<b>⚠️ ПРЕДУПРЕЖДЕНИЕ:</b> SSL сертификат скоро истечет!
                
Домен: ${DOMAIN}
Истекает: ${SSL_EXPIRY}
Осталось дней: ${DAYS_LEFT}
Время: $(date '+%Y-%m-%d %H:%M:%S')
                
Рекомендация:
Обновить сертификат: <code>certbot renew</code>" "⚠️"
            fi
        else
            echo "✅ SSL: истекает через ${DAYS_LEFT} дней"
        fi
    fi
fi

echo "✅ Проверки завершены: $(date '+%Y-%m-%d %H:%M:%S')"
