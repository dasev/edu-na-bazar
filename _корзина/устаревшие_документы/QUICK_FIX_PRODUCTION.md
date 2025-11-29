# ⚡ Быстрое исправление production

## 🎯 Проблема
Backend на сервере 176.99.5.211 не отвечает

## ✅ Локально все работает
- Backend: http://localhost:8000/health → OK
- БД: 22 товара, категории, магазины
- Миграции: применены (8828a8665651)

---

## 🚀 Решение за 5 минут

### 1. Подключиться к серверу
```bash
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL
```

### 2. Проверить контейнеры
```bash
cd /opt/edu-na-bazar
docker-compose ps
```

**Если контейнеры не запущены:**
```bash
docker-compose up -d
```

### 3. Проверить логи backend
```bash
docker-compose logs backend --tail=50
```

**Типичные ошибки:**

#### ❌ "relation products does not exist"
**Решение:** Применить миграции
```bash
docker-compose exec backend alembic upgrade head
```

#### ❌ "could not connect to database"
**Решение:** Проверить .env и перезапустить
```bash
cat .env | grep POSTGRES
docker-compose restart postgres
sleep 10
docker-compose restart backend
```

#### ❌ ".env file not found"
**Решение:** Создать .env
```bash
cp .env.example .env
nano .env
# Установить:
# - POSTGRES_PASSWORD (openssl rand -base64 24)
# - SECRET_KEY (python3 -c "import secrets; print(secrets.token_urlsafe(32))")
# - ALLOWED_ORIGINS=http://176.99.5.211
docker-compose down
docker-compose up -d
```

### 4. Проверить БД
```bash
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.products"
```

**Если БД пустая:**
```bash
# На локальной машине:
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > dump.sql
scp dump.sql root@176.99.5.211:/tmp/

# На сервере:
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql
```

### 5. Проверить работу
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/categories/
```

**Должно вернуть JSON без ошибок**

### 6. Проверить firewall
```bash
ufw allow 8000/tcp
ufw allow 80/tcp
```

### 7. Проверить из браузера
- http://176.99.5.211:8000/health
- http://176.99.5.211:8000/api/categories/
- http://176.99.5.211

---

## 🔥 Если ничего не помогло - полный перезапуск

```bash
cd /opt/edu-na-bazar

# Остановить все
docker-compose down

# Убедиться что .env существует
ls -la .env

# Запустить заново
docker-compose up -d --build

# Подождать
sleep 30

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить
docker-compose ps
docker-compose logs backend --tail=20
curl http://localhost:8000/health
```

---

## 📋 Минимальный .env для production

```env
ENVIRONMENT=production
POSTGRES_DB=edu_na_bazar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш_сильный_пароль
REDIS_URL=redis://redis:6379/0
SECRET_KEY=ваш_секретный_ключ_32_символа
ALLOWED_ORIGINS=http://176.99.5.211,http://localhost
SMS_ENABLED=false
REACT_APP_API_URL=http://176.99.5.211:8000
```

---

## ✅ Критерии успеха

1. `docker-compose ps` - все контейнеры UP
2. `curl http://localhost:8000/health` - {"status":"ok"}
3. `curl http://localhost:8000/api/categories/` - JSON с категориями
4. http://176.99.5.211:8000/health - открывается в браузере
5. http://176.99.5.211 - показывает frontend

---

**Время на исправление: 5-10 минут**
