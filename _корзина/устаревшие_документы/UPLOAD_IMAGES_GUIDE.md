# 📸 Руководство по загрузке изображений на production

## 📋 Проблема

Изображения товаров находятся только локально в `backend/uploads/products/original/`.
В production используется named volume, поэтому файлы нужно загрузить отдельно.

---

## 🎯 Решения

### Вариант 1: Архив для загрузки на сервер (Рекомендуется)

#### Шаг 1: Создать архив локально

**Windows (PowerShell):**
```powershell
# Перейти в папку проекта
cd C:\python\edu-na-bazar

# Создать архив
Compress-Archive -Path backend\uploads\* -DestinationPath uploads.zip

# Или использовать 7-Zip (если установлен)
7z a -tzip uploads.zip backend\uploads\*
```

**Linux/Mac:**
```bash
cd /path/to/edu-na-bazar
tar -czf uploads.tar.gz backend/uploads/
```

#### Шаг 2: Загрузить на сервер

```bash
# Загрузить архив на сервер
scp uploads.zip root@your_server_ip:/opt/edu-na-bazar/

# Или через WinSCP, FileZilla, etc.
```

#### Шаг 3: Распаковать на сервере

```bash
# Подключиться к серверу
ssh root@your_server_ip

# Перейти в директорию проекта
cd /opt/edu-na-bazar

# Распаковать архив
unzip uploads.zip
# или
tar -xzf uploads.tar.gz

# Скопировать в volume контейнера
docker cp backend/uploads/. edu-na-bazar-backend:/app/uploads/

# Проверить
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/
```

---

### Вариант 2: S3/CloudStorage (Для больших проектов)

Использовать облачное хранилище вместо локальных файлов.

#### AWS S3

**1. Создать S3 bucket:**
```bash
aws s3 mb s3://edunabazar-uploads
aws s3api put-bucket-cors --bucket edunabazar-uploads --cors-configuration file://cors.json
```

**cors.json:**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://yourdomain.com"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"]
    }
  ]
}
```

**2. Загрузить файлы:**
```bash
aws s3 sync backend/uploads/ s3://edunabazar-uploads/ --acl public-read
```

**3. Обновить пути в БД:**
```sql
UPDATE market.products 
SET image = REPLACE(image, '/uploads/', 'https://edunabazar-uploads.s3.amazonaws.com/');

UPDATE market.product_images 
SET image_url = REPLACE(image_url, '/uploads/', 'https://edunabazar-uploads.s3.amazonaws.com/');
```

**4. Обновить код (опционально):**
```python
# backend/config.py
UPLOADS_URL = os.getenv("UPLOADS_URL", "/uploads")  # или S3 URL

# backend/api/routers/images.py
# Использовать UPLOADS_URL вместо /uploads
```

#### DigitalOcean Spaces

```bash
# Установить s3cmd
apt install s3cmd

# Настроить
s3cmd --configure

# Загрузить
s3cmd sync backend/uploads/ s3://edunabazar-uploads/
```

#### Cloudflare R2 (Дешевле S3)

```bash
# Установить rclone
curl https://rclone.org/install.sh | sudo bash

# Настроить
rclone config

# Загрузить
rclone sync backend/uploads/ r2:edunabazar-uploads/
```

---

### Вариант 3: Прямая загрузка через Docker

Если контейнеры уже запущены:

```bash
# На локальной машине создать архив
tar -czf uploads.tar.gz backend/uploads/

# Загрузить на сервер
scp uploads.tar.gz root@your_server_ip:/tmp/

# На сервере
ssh root@your_server_ip

# Распаковать в контейнер
docker cp /tmp/uploads.tar.gz edu-na-bazar-backend:/tmp/
docker exec edu-na-bazar-backend tar -xzf /tmp/uploads.tar.gz -C /app/
docker exec edu-na-bazar-backend rm /tmp/uploads.tar.gz

# Проверить
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/
```

---

### Вариант 4: Bind Mount в Production (Не рекомендуется)

Изменить `docker-compose.yml` для использования bind mount:

```yaml
# docker-compose.yml
backend:
  volumes:
    - ./backend/uploads:/app/uploads  # Bind mount вместо named volume
```

**Минусы:**
- Нужно загружать файлы на хост
- Меньше изоляции
- Сложнее управлять правами доступа

---

## 📊 Сравнение вариантов

| Вариант | Сложность | Стоимость | Масштабируемость | Рекомендация |
|---------|-----------|-----------|------------------|--------------|
| **Архив на сервер** | ⭐ Легко | 💰 Бесплатно | ⚠️ Ограничена | ✅ Для старта |
| **AWS S3** | ⭐⭐ Средне | 💰💰 ~$0.023/GB | ✅ Отлично | ✅ Для роста |
| **DigitalOcean Spaces** | ⭐⭐ Средне | 💰💰 $5/250GB | ✅ Хорошо | ✅ Для среднего |
| **Cloudflare R2** | ⭐⭐ Средне | 💰 $0.015/GB | ✅ Отлично | ✅ Самый дешевый |
| **Bind Mount** | ⭐ Легко | 💰 Бесплатно | ⚠️ Плохо | ❌ Не рекомендуется |

---

## 🚀 Быстрый старт (Рекомендуемый способ)

### На локальной машине:

```powershell
# 1. Создать архив
cd C:\python\edu-na-bazar
Compress-Archive -Path backend\uploads\* -DestinationPath uploads.zip

# 2. Проверить размер
Get-Item uploads.zip | Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}
```

### На сервере:

```bash
# 1. Загрузить архив (через FileZilla, WinSCP или scp)
# 2. Распаковать в контейнер
cd /opt/edu-na-bazar
docker cp uploads.zip edu-na-bazar-backend:/tmp/
docker exec edu-na-bazar-backend unzip /tmp/uploads.zip -d /app/
docker exec edu-na-bazar-backend rm /tmp/uploads.zip

# 3. Проверить
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/ | head -20

# 4. Проверить доступ через API
curl http://localhost:8000/uploads/products/original/021a631edfe6b4b3a2bcc0ab7df444d1.jpg -I
```

---

## ✅ Проверка

После загрузки проверьте:

```bash
# 1. Файлы в контейнере
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/ | wc -l

# 2. Доступ через API
curl http://your_domain/uploads/products/original/test.jpg -I

# 3. Доступ через frontend
# Откройте сайт и проверьте отображение изображений товаров
```

---

## 🔧 Troubleshooting

### Проблема: Изображения не отображаются

**Проверить:**
```bash
# 1. Файлы существуют
docker exec edu-na-bazar-backend ls /app/uploads/products/original/

# 2. Права доступа
docker exec edu-na-bazar-backend ls -la /app/uploads/

# 3. Nginx отдает файлы
docker logs edu-na-bazar-backend | grep uploads
```

**Исправить права:**
```bash
docker exec edu-na-bazar-backend chmod -R 755 /app/uploads/
```

### Проблема: 404 Not Found

**Проверить пути в БД:**
```sql
SELECT image FROM market.products LIMIT 5;
-- Должно быть: /uploads/products/original/filename.jpg
```

**Исправить пути:**
```sql
UPDATE market.products 
SET image = CONCAT('/uploads/products/original/', image)
WHERE image NOT LIKE '/uploads/%';
```

---

## 📝 Checklist

- [ ] Создан архив с изображениями
- [ ] Архив загружен на сервер
- [ ] Файлы распакованы в контейнер
- [ ] Проверены права доступа (755)
- [ ] Проверен доступ через API
- [ ] Проверено отображение на сайте
- [ ] Создан backup архива
- [ ] Документирован процесс

---

## 💡 Рекомендации

1. **Для старта**: Используйте архив на сервере
2. **При росте**: Переходите на S3/Cloudflare R2
3. **Backup**: Храните архив с изображениями отдельно
4. **Оптимизация**: Используйте CDN для ускорения загрузки
5. **Сжатие**: Оптимизируйте изображения перед загрузкой

---

**Создано**: 25.11.2025  
**Статус**: ✅ Готово к использованию
