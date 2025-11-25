# 📋 Команды для деплоя - Копируй и Вставляй

## Шаг 1: На вашей машине (PowerShell)

Откройте PowerShell и скопируйте эти команды:

```powershell
# Перейти в папку проекта
cd C:\python\edu-na-bazar

# Загрузить скрипт на сервер
scp FULL_DEPLOY.sh root@176.99.5.211:/root/
```

**Пароль**: `sIAS6APDsKh0bL`

---

## Шаг 2: Подключиться к серверу

```powershell
ssh root@176.99.5.211
```

**Пароль**: `sIAS6APDsKh0bL`

---

## Шаг 3: На сервере - скопируйте ВСЕ команды сразу

После подключения к серверу скопируйте и вставьте этот блок целиком:

```bash
# Запустить деплой
cd /root
bash FULL_DEPLOY.sh << 'EOF'
https://github.com/your-username/edu-na-bazar.git
EOF
```

⚠️ **ВАЖНО**: Замените `your-username` на ваш GitHub username!

Или если репозитория нет, используйте этот вариант:

```bash
# Установка без Git (загрузка архива)
cd /root

# Обновление системы
apt update && apt upgrade -y
apt install -y curl git nano htop wget unzip

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh
systemctl enable docker
systemctl start docker

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверка
docker --version
docker-compose --version

echo "✅ Docker установлен! Теперь загрузите проект."
```

---

## Шаг 4: Загрузить проект (если нет Git)

**На вашей машине (PowerShell):**

```powershell
# Создать архив проекта
cd C:\python\edu-na-bazar
tar.exe -czf edu-na-bazar.tar.gz --exclude=node_modules --exclude=venv --exclude=__pycache__ --exclude=.git --exclude=frontend/node_modules --exclude=backend/venv .

# Загрузить на сервер
scp edu-na-bazar.tar.gz root@176.99.5.211:/opt/
```

**На сервере:**

```bash
# Распаковать проект
cd /opt
tar -xzf edu-na-bazar.tar.gz
mkdir -p edu-na-bazar
tar -xzf edu-na-bazar.tar.gz -C edu-na-bazar
cd edu-na-bazar

# Создать .env
cp .env.example .env

# Сгенерировать пароли
SECRET_KEY=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -base64 24)

# Обновить .env
sed -i "s/your-secret-key-here-min-32-chars-use-openssl-rand-hex-32/$SECRET_KEY/" .env
sed -i "s/your_secure_postgres_password_here/$DB_PASSWORD/" .env
sed -i "s/ENVIRONMENT=development/ENVIRONMENT=production/" .env
sed -i "s|ALLOWED_ORIGINS=.*|ALLOWED_ORIGINS=http://176.99.5.211,http://localhost|" .env
sed -i "s|REACT_APP_API_URL=.*|REACT_APP_API_URL=http://176.99.5.211:8000|" .env

echo "✅ .env создан"
echo "SECRET_KEY: $SECRET_KEY"
echo "DB_PASSWORD: $DB_PASSWORD"

# Запустить контейнеры
docker-compose up -d --build

# Подождать запуска
sleep 30

# Применить миграции
docker-compose exec -T backend alembic upgrade head

# Настроить firewall
apt install -y ufw
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw allow 3000/tcp
ufw --force enable

# Создать директории
mkdir -p /backups

# Проверка
docker-compose ps
curl http://localhost:8000/api/health

echo ""
echo "========================================="
echo "✅ ДЕПЛОЙ ЗАВЕРШЕН!"
echo "========================================="
echo ""
echo "🌐 Откройте в браузере:"
echo "   http://176.99.5.211"
echo "   http://176.99.5.211:8000/api/health"
echo ""
```

---

## Шаг 5: Загрузить изображения

**На вашей машине:**

```powershell
cd C:\python\edu-na-bazar
.\CREATE_UPLOADS_ARCHIVE.bat
scp uploads.zip root@176.99.5.211:/opt/edu-na-bazar/
```

**На сервере:**

```bash
cd /opt/edu-na-bazar
docker cp uploads.zip edu-na-bazar-backend:/tmp/
docker exec edu-na-bazar-backend unzip -o /tmp/uploads.zip -d /app/
docker exec edu-na-bazar-backend rm /tmp/uploads.zip
docker exec edu-na-bazar-backend chmod -R 755 /app/uploads/

echo "✅ Изображения загружены!"
```

---

## ✅ Готово!

Откройте в браузере: **http://176.99.5.211**

---

## 🐛 Если что-то не работает

```bash
# Посмотреть логи
docker-compose logs -f backend

# Перезапустить
docker-compose restart

# Проверить контейнеры
docker-compose ps
```
