# 🖼️ План миграции изображений

## 📊 Текущая ситуация

### temp.file:
- **Всего изображений:** 9,765
- **С привязкой к товару (advert_id):** 0 ⚠️
- **С привязкой к компании (company_id):** 0 ⚠️

**Проблема:** Изображения не привязаны к товарам!

### market.product_images:
```sql
id          BIGINT      -- ID изображения
product_id  BIGINT      -- Товар (FK)
image_url   TEXT        -- URL изображения
sort_order  INTEGER     -- Порядок сортировки
created_at  TIMESTAMP   -- Дата создания
```

---

## 🎯 Решение

### 1. Добавим поле old_id для отслеживания
```sql
ALTER TABLE market.product_images 
ADD COLUMN old_id INTEGER;  -- ID из temp.file
```

### 2. Структура каталогов для изображений

```
backend/
└── uploads/
    └── products/
        ├── original/           ← Оригинальные изображения
        ├── thumbnails/         ← Миниатюры (автогенерация)
        └── optimized/          ← Оптимизированные (автогенерация)
```

**URL на фронте:**
- Оригинал: `/uploads/products/original/filename.jpg`
- Миниатюра: `/uploads/products/thumbnails/filename.jpg`
- Оптимизированное: `/uploads/products/optimized/filename.jpg`

---

## 🔧 Варианты миграции изображений

### Вариант 1: Без привязки к товарам ❌
Пропустить миграцию изображений, т.к. нет связи с товарами.

**Минусы:** Потеряем 9,765 изображений

### Вариант 2: Случайное распределение ⚠️
Распределить изображения случайным образом по товарам.

**Минусы:** Неправильные изображения у товаров

### Вариант 3: По имени файла 🤔
Попытаться найти связь через имя файла или путь.

**Плюсы:** Может сработать если есть паттерн  
**Минусы:** Ненадёжно

### Вариант 4: Первое изображение каждому товару ✅ РЕКОМЕНДУЮ
Назначить каждому товару первое доступное изображение.

**Плюсы:** 
- Все товары с изображениями
- Простая логика
- Можно потом вручную исправить

**Минусы:** 
- Изображения могут не соответствовать товарам
- Требуется ручная корректировка

### Вариант 5: Пропустить сейчас, добавить позже ✅ БЕЗОПАСНО
Не мигрировать изображения, добавить их позже вручную или через админку.

**Плюсы:**
- Безопасно
- Можно загрузить правильные изображения
- Не будет путаницы

---

## 💡 Моя рекомендация

### Вариант 4 + 5 (Комбинированный):

1. **Создать структуру каталогов** `uploads/products/`
2. **Добавить поле old_id** в `market.product_images`
3. **Скопировать файлы** из старой системы в `uploads/products/original/`
4. **Создать таблицу маппинга** `temp.image_mapping` для ручной корректировки
5. **Назначить плейсхолдеры** товарам без изображений

**Преимущества:**
- Файлы сохранены
- Можно вручную исправить через SQL
- Есть плейсхолдеры для товаров
- Поле old_id для отслеживания

---

## 🚀 Реализация

### Шаг 1: Подготовка структуры

```sql
-- Добавляем поле old_id
ALTER TABLE market.product_images 
ADD COLUMN IF NOT EXISTS old_id INTEGER;

-- Создаём индекс
CREATE INDEX IF NOT EXISTS idx_product_images_old_id 
ON market.product_images(old_id);
```

### Шаг 2: Создание каталогов

```python
from pathlib import Path

# Создаём структуру
Path("uploads/products/original").mkdir(parents=True, exist_ok=True)
Path("uploads/products/thumbnails").mkdir(parents=True, exist_ok=True)
Path("uploads/products/optimized").mkdir(parents=True, exist_ok=True)
```

### Шаг 3: Копирование файлов

```python
# Копируем файлы из старой системы
# Источник: /path/to/old/uploads/
# Назначение: uploads/products/original/

import shutil
from pathlib import Path

old_path = Path("/path/to/old/uploads")
new_path = Path("uploads/products/original")

for file in old_path.glob("*.jpg"):
    shutil.copy2(file, new_path / file.name)
```

### Шаг 4: Создание таблицы маппинга

```sql
-- Таблица для ручной корректировки
CREATE TABLE IF NOT EXISTS temp.image_mapping (
    old_file_id INTEGER PRIMARY KEY,
    old_filename VARCHAR(255),
    old_path VARCHAR(255),
    new_product_id BIGINT,
    new_image_id BIGINT,
    is_correct BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- Заполняем из temp.file
INSERT INTO temp.image_mapping (old_file_id, old_filename, old_path)
SELECT id, filename, path
FROM temp.file
WHERE type = 'image';
```

### Шаг 5: Назначение плейсхолдеров

```sql
-- Вставляем плейсхолдер для каждого товара
INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
SELECT 
    p.id as product_id,
    '/uploads/products/placeholder.jpg' as image_url,
    NULL as old_id,
    0 as sort_order,
    NOW() as created_at
FROM market.products p
WHERE NOT EXISTS (
    SELECT 1 FROM market.product_images pi WHERE pi.product_id = p.id
);
```

---

## 📋 SQL для ручной корректировки

### Назначить изображение товару:

```sql
-- 1. Найти товар и изображение
SELECT id, name FROM market.products WHERE name LIKE '%яблоки%';
SELECT old_file_id, old_filename FROM temp.image_mapping WHERE old_filename LIKE '%apple%';

-- 2. Обновить изображение товара
UPDATE market.product_images 
SET image_url = '/uploads/products/original/apple.jpg',
    old_id = 123  -- ID из temp.file
WHERE product_id = 456;

-- 3. Отметить в маппинге
UPDATE temp.image_mapping
SET new_product_id = 456,
    new_image_id = (SELECT id FROM market.product_images WHERE product_id = 456),
    is_correct = TRUE,
    notes = 'Назначено вручную'
WHERE old_file_id = 123;
```

### Массовое назначение по паттерну:

```sql
-- Если есть паттерн в именах файлов
UPDATE market.product_images pi
SET image_url = '/uploads/products/original/' || im.old_filename,
    old_id = im.old_file_id
FROM temp.image_mapping im
JOIN market.products p ON p.name ILIKE '%' || SUBSTRING(im.old_filename, 1, 10) || '%'
WHERE pi.product_id = p.id
  AND im.new_product_id IS NULL;
```

---

## 📊 Статистика после миграции

```sql
-- Товары с изображениями
SELECT 
    COUNT(*) as total_products,
    COUNT(CASE WHEN pi.id IS NOT NULL THEN 1 END) as with_images,
    COUNT(CASE WHEN pi.image_url LIKE '%placeholder%' THEN 1 END) as with_placeholder
FROM market.products p
LEFT JOIN market.product_images pi ON pi.product_id = p.id;

-- Прогресс корректировки
SELECT 
    COUNT(*) as total_images,
    COUNT(CASE WHEN is_correct THEN 1 END) as corrected,
    COUNT(CASE WHEN new_product_id IS NOT NULL THEN 1 END) as assigned
FROM temp.image_mapping;
```

---

## 🎯 Итоговый план

1. ✅ Добавить поле `old_id` в `market.product_images`
2. ✅ Создать структуру каталогов `uploads/products/`
3. ✅ Создать таблицу `temp.image_mapping` для отслеживания
4. ✅ Скопировать файлы в `uploads/products/original/`
5. ✅ Назначить плейсхолдеры всем товарам
6. ⏳ Вручную исправить через SQL (постепенно)

---

## 🔧 Скрипт миграции

Создам обновлённый скрипт `migrate_images.py` который:
- Добавит поле old_id
- Создаст каталоги
- Создаст таблицу маппинга
- Назначит плейсхолдеры
- Сохранит информацию для ручной корректировки

---

**Согласны с этим подходом?** 🤔
