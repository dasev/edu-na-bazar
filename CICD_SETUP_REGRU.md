# 🔄 CI/CD Setup для REG.RU через GitHub Actions

## 🎯 Что это дает

После настройки CI/CD каждый `git push` в ветку `main` будет автоматически:
1. ✅ Собирать Docker образы
2. ✅ Загружать их в Docker Hub
3. ✅ Создавать backup БД на сервере
4. ✅ Обновлять код на сервере
5. ✅ Перезапускать контейнеры
6. ✅ Применять миграции БД
7. ✅ Проверять работоспособность (health check)
8. ✅ Показывать результат деплоя

**Время деплоя: 3-5 минут автоматически!**

---

## 📋 Что нужно

- ✅ Проект на GitHub
- ✅ Аккаунт на Docker Hub (бесплатно)
- ✅ Сервер на REG.RU с развернутым проектом
- ✅ SSH доступ к серверу

---

## 🚀 Этап 1: Настройка Docker Hub (5 минут)

### 1. Создать аккаунт:
- Перейти на https://hub.docker.com
- Sign Up (бесплатно)
- Подтвердить email

### 2. Создать Access Token:
```
1. Войти в Docker Hub
2. Account Settings → Security → New Access Token
3. Description: "GitHub Actions"
4. Access permissions: Read, Write, Delete
5. Generate
6. СКОПИРОВАТЬ токен (показывается один раз!)
```

---

## 🔑 Этап 2: Настройка SSH ключа (5 минут)

### На локальной машине:

```powershell
# Сгенерировать SSH ключ (если нет)
ssh-keygen -t ed25519 -C "github-actions" -f github_actions_key

# Будет создано 2 файла:
# - github_actions_key (приватный ключ)
# - github_actions_key.pub (публичный ключ)

# Скопировать публичный ключ
Get-Content github_actions_key.pub | clip
```

### На сервере REG.RU:

```bash
# Подключиться к серверу
ssh root@YOUR_SERVER_IP

# Добавить публичный ключ
nano ~/.ssh/authorized_keys
# Вставить скопированный ключ на новую строку
# Сохранить (Ctrl+X, Y, Enter)

# Установить правильные права
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### Проверить подключение:

```powershell
# На локальной машине
ssh -i github_actions_key root@YOUR_SERVER_IP

# Должно подключиться без пароля
```

---

## 🔐 Этап 3: Настройка GitHub Secrets (5 минут)

### В репозитории GitHub:

```
1. Открыть репозиторий на GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
```

### Добавить следующие секреты:

#### 1. DOCKER_USERNAME
```
Name: DOCKER_USERNAME
Secret: ваш_username_на_docker_hub
```

#### 2. DOCKER_PASSWORD
```
Name: DOCKER_PASSWORD
Secret: токен_из_docker_hub (из Этапа 1)
```

#### 3. SERVER_HOST
```
Name: SERVER_HOST
Secret: IP_адрес_сервера_REG.RU
Пример: 123.45.67.89
```

#### 4. SERVER_USER
```
Name: SERVER_USER
Secret: root
```

#### 5. SSH_PRIVATE_KEY
```
Name: SSH_PRIVATE_KEY
Secret: содержимое файла github_actions_key (приватный ключ)

# На Windows:
Get-Content github_actions_key | clip

# Вставить весь текст включая:
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

#### 6. API_URL (опционально)
```
Name: API_URL
Secret: https://yourdomain.ru
```

### Итого должно быть 5-6 секретов:
- ✅ DOCKER_USERNAME
- ✅ DOCKER_PASSWORD
- ✅ SERVER_HOST
- ✅ SERVER_USER
- ✅ SSH_PRIVATE_KEY
- ✅ API_URL (опционально)

---

## 📦 Этап 4: Подготовка сервера (5 минут)

### На сервере REG.RU:

```bash
# 1. Убедиться что проект клонирован через Git
cd /opt/edu-na-bazar
git remote -v
# Должно показать ваш GitHub репозиторий

# Если проект не через Git:
cd /opt
rm -rf edu-na-bazar
git clone https://github.com/YOUR_USERNAME/edu-na-bazar.git
cd edu-na-bazar

# 2. Создать директорию для backup
mkdir -p /backups

# 3. Настроить Git (чтобы не было конфликтов)
git config --global pull.rebase false
git config --global user.email "server@yourdomain.ru"
git config --global user.name "Production Server"

# 4. Убедиться что .env файл на месте
ls -la .env
# Если нет - создать из .env.example

# 5. Проверить что контейнеры запущены
docker-compose ps
```

---

## 🔧 Этап 5: Обновление docker-compose.yml (5 минут)

### Использовать образы из Docker Hub:

```bash
# На сервере
cd /opt/edu-na-bazar
nano docker-compose.yml
```

### Изменить секции backend и frontend:

```yaml
services:
  backend:
    image: YOUR_DOCKER_USERNAME/edu-na-bazar-backend:latest
    # Убрать build секцию
    container_name: edu-na-bazar-backend
    environment:
      # ... остальное без изменений
    # ... остальное без изменений

  frontend:
    image: YOUR_DOCKER_USERNAME/edu-na-bazar-frontend:latest
    # Убрать build секцию
    container_name: edu-na-bazar-frontend
    # ... остальное без изменений
```

### Сохранить и перезапустить:

```bash
# Сохранить (Ctrl+X, Y, Enter)

# Перезапустить с новыми образами
docker-compose down
docker-compose pull
docker-compose up -d
```

---

## ✅ Этап 6: Тестирование CI/CD (5 минут)

### 1. Сделать тестовый коммит:

```bash
# На локальной машине
cd C:\python\edu-na-bazar

# Внести изменение
echo "# CI/CD Test" >> README.md

# Закоммитить
git add .
git commit -m "test: CI/CD deployment"
git push origin main
```

### 2. Проверить GitHub Actions:

```
1. Открыть репозиторий на GitHub
2. Перейти в Actions
3. Увидеть запущенный workflow "Deploy to Production"
4. Кликнуть на него для просмотра логов
```

### 3. Наблюдать процесс:

```
✅ Checkout code
✅ Set up Docker Buildx
✅ Login to Docker Hub
✅ Build and push Backend (2-3 минуты)
✅ Build and push Frontend (2-3 минуты)
✅ Deploy to Server (1 минута)
✅ Health Check (30 секунд)
✅ Deployment Summary
```

### 4. Проверить на сервере:

```bash
# Подключиться к серверу
ssh root@YOUR_SERVER_IP

# Проверить что обновилось
cd /opt/edu-na-bazar
git log -1

# Проверить контейнеры
docker-compose ps

# Проверить логи
docker-compose logs -f backend
```

---

## 🎉 Готово!

Теперь при каждом `git push` в `main`:
1. Код автоматически деплоится на сервер
2. Создается backup БД
3. Применяются миграции
4. Проверяется работоспособность

---

## 📊 Workflow деплоя

```
┌─────────────────┐
│  git push main  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  GitHub Actions Start   │
└────────┬────────────────┘
         │
         ├─► 🏗️ Build Backend Image (2-3 мин)
         │
         ├─► 🏗️ Build Frontend Image (2-3 мин)
         │
         ├─► 📤 Push to Docker Hub
         │
         ▼
┌─────────────────────────┐
│  Deploy to Server       │
├─────────────────────────┤
│ 1. 💾 Create Backup     │
│ 2. 📥 Pull Code         │
│ 3. 🐳 Pull Images       │
│ 4. 🛑 Stop Containers   │
│ 5. 🚀 Start New         │
│ 6. 🔄 Run Migrations    │
│ 7. 🧹 Cleanup           │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Health Check           │
├─────────────────────────┤
│ ✅ API: /api/health     │
│ ✅ Frontend: /          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  ✅ Success!            │
│  🌐 Site Updated        │
└─────────────────────────┘
```

---

## 🔧 Дополнительные настройки

### Деплой только при тегах (опционально):

```yaml
# .github/workflows/deploy.yml
on:
  push:
    tags:
      - 'v*'  # Деплой только при тегах v1.0.0, v1.1.0 и т.д.
```

### Уведомления в Telegram (опционально):

Добавить в конец `.github/workflows/deploy.yml`:

```yaml
    - name: 📱 Notify Telegram
      if: always()
      uses: appleboy/telegram-action@master
      with:
        to: ${{ secrets.TELEGRAM_CHAT_ID }}
        token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        message: |
          🚀 Deployment ${{ job.status }}!
          
          Repository: ${{ github.repository }}
          Branch: ${{ github.ref }}
          Commit: ${{ github.sha }}
          Author: ${{ github.actor }}
          
          ${{ job.status == 'success' && '✅ Successfully deployed!' || '❌ Deployment failed!' }}
```

Добавить секреты:
- `TELEGRAM_BOT_TOKEN` - токен бота
- `TELEGRAM_CHAT_ID` - ID чата

---

## 🐛 Troubleshooting

### Ошибка: "Permission denied (publickey)"

```bash
# Проверить SSH ключ на сервере
cat ~/.ssh/authorized_keys

# Проверить права
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Проверить подключение вручную
ssh -i github_actions_key root@YOUR_SERVER_IP
```

### Ошибка: "docker-compose: command not found"

```bash
# На сервере установить docker-compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### Ошибка: "Cannot connect to Docker daemon"

```bash
# На сервере
systemctl start docker
systemctl enable docker
```

### Ошибка при миграциях

```bash
# На сервере проверить
docker-compose exec backend alembic current
docker-compose logs backend

# Применить вручную
docker-compose exec backend alembic upgrade head
```

### Workflow не запускается

```
1. Проверить что файл .github/workflows/deploy.yml в main ветке
2. Проверить что все секреты добавлены в GitHub
3. Проверить что Actions включены: Settings → Actions → Allow all actions
```

---

## 📝 Полезные команды

### Локально:

```bash
# Посмотреть статус workflow
gh run list  # Требует GitHub CLI

# Посмотреть логи последнего run
gh run view --log

# Запустить workflow вручную
gh workflow run deploy.yml
```

### На сервере:

```bash
# Посмотреть последние деплои
ls -lt /backups/ | head -10

# Откатиться на предыдущую версию
cd /opt/edu-na-bazar
git log --oneline -10
git reset --hard COMMIT_HASH
docker-compose up -d --force-recreate

# Восстановить БД из backup
docker-compose exec -T postgres psql -U postgres edu_na_bazar < /backups/backup.sql
```

---

## ✅ Checklist настройки CI/CD

- [ ] Создан аккаунт на Docker Hub
- [ ] Создан Access Token в Docker Hub
- [ ] Сгенерирован SSH ключ
- [ ] Публичный ключ добавлен на сервер
- [ ] Все 5-6 секретов добавлены в GitHub
- [ ] docker-compose.yml обновлен для использования образов
- [ ] Проект на сервере клонирован через Git
- [ ] Создана директория /backups
- [ ] Тестовый деплой прошел успешно
- [ ] Health check работает
- [ ] Backup создается автоматически

---

## 🎯 Результат

После настройки CI/CD:
- ✅ Автоматический деплой при каждом push
- ✅ Backup перед каждым деплоем
- ✅ Автоматические миграции БД
- ✅ Health check после деплоя
- ✅ История деплоев в GitHub Actions
- ✅ Откат на предыдущую версию одной командой

**Время деплоя: 3-5 минут автоматически!**

---

**Создано**: 25.11.2025  
**Время настройки**: 30 минут  
**Статус**: ✅ Готово к использованию
