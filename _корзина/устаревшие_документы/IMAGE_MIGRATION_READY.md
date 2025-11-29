# ✅ Миграция изображений готова!

## 🎯 Что реализовано

### 1. Поле old_id для отслеживания
```sql
market.product_images:
├── id          BIGINT      -- Новый ID
├── product_id  BIGINT      -- Товар
├── image_url   TEXT        -- URL изображения
├── old_id      INTEGER     -- ✅ ID из temp.file (для ручной корректировки)
├── sort_order  INTEGER     -- Порядок
└── created_at  TIMESTAMP   -- Дата
```

### 2. Таблица маппинга для ручной корректировки
```sql
temp.image_mapping:
├── old_file_id     INTEGER     -- ID из temp.file
├── old_filename    VARCHAR     -- Имя файла
├── old_path        VARCHAR     -- Путь
├── new_product_id  BIGINT      -- Новый ID товара
├── new_image_id    BIGINT      -- Новый ID изображения
├── is_correct      BOOLEAN     -- Правильно ли назначено
└── notes           TEXT        -- Заметки
```

### 3. Структура каталогов
```
backend/
└── uploads/
    └── products/
        ├── original/           ← Оригинальные изображения
        ├── thumbnails/         ← Миниатюры (автогенерация)
        ├── optimized/          ← Оптимизированные (автогенерация)
        └── placeholder.jpg     ← Плейсхолдер
```

---

## 📋 Порядок работы с изображениями

### Шаг 1: Настройка структуры (ПЕРЕД миграцией)
```bash
cd backend
python scripts\setup_images.py
```

**Что произойдёт:**
- ✅ Создадутся каталоги `uploads/products/`
- ✅ Добавится поле `old_id` в `market.product_images`
- ✅ Создастся таблица `temp.image_mapping`
- ✅ Заполнится маппинг из `temp.file` (9,765 записей)

### Шаг 2: Копирование файлов (ВРУЧНУЮ)
```bash
# Скопируйте файлы из старой системы в:
uploads/products/original/

# Например:
copy "D:\old_system\uploads\*.jpg" "uploads\products\original\"
```

### Шаг 3: Миграция данных
```bash
run_migration.bat
```

**Что произойдёт:**
- Т.к. в `temp.file` нет привязки к товарам (`advert_id = NULL`)
- Каждому товару назначится плейсхолдер `/uploads/products/placeholder.jpg`
- Сохранится информация в `temp.image_mapping` для ручной корректировки

---

## 🔧 Ручная корректировка через SQL

### 1. Просмотр доступных изображений
```sql
-- Все изображения из temp
SELECT old_file_id, old_filename, old_path
FROM temp.image_mapping
WHERE new_product_id IS NULL
ORDER BY old_filename
LIMIT 50;
```

### 2. Поиск товара
```sql
-- Найти товар по названию
SELECT id, name 
FROM market.products 
WHERE name ILIKE '%яблоки%'
LIMIT 10;
```

### 3. Назначение изображения товару
```sql
-- Обновить изображение товара
UPDATE market.product_images 
SET image_url = '/uploads/products/original/apple_123.jpg',
    old_id = 456  -- ID из temp.file
WHERE product_id = 789;

-- Отметить в маппинге
UPDATE temp.image_mapping
SET new_product_id = 789,
    new_image_id = (SELECT id FROM market.product_images WHERE product_id = 789 LIMIT 1),
    is_correct = TRUE,
    notes = 'Назначено вручную 2025-11-24'
WHERE old_file_id = 456;
```

### 4. Массовое назначение по паттерну
```sql
-- Если в именах файлов есть ID товара
UPDATE market.product_images pi
SET image_url = '/uploads/products/original/' || im.old_filename,
    old_id = im.old_file_id
FROM temp.image_mapping im
JOIN market.products p ON CAST(SUBSTRING(im.old_filename FROM '\d+') AS INTEGER) = p.id
WHERE pi.product_id = p.id
  AND im.new_product_id IS NULL;
```

### 5. Добавление дополнительных изображений
```sql
-- Добавить ещё одно изображение к товару
INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
VALUES (
    789,  -- ID товара
    '/uploads/products/original/apple_456.jpg',
    456,  -- old_id из temp.file
    1,    -- Второе изображение
    NOW()
);

-- Обновить маппинг
UPDATE temp.image_mapping
SET new_product_id = 789,
    new_image_id = CURRVAL('market.product_images_id_seq'),
    is_correct = TRUE
WHERE old_file_id = 456;
```

---

## 📊 Статистика и проверки

### Прогресс корректировки
```sql
SELECT 
    COUNT(*) as total_images,
    COUNT(CASE WHEN new_product_id IS NOT NULL THEN 1 END) as assigned,
    COUNT(CASE WHEN is_correct THEN 1 END) as verified,
    ROUND(COUNT(CASE WHEN new_product_id IS NOT NULL THEN 1 END)::NUMERIC / COUNT(*) * 100, 2) as progress_percent
FROM temp.image_mapping;
```

### Товары без изображений
```sql
SELECT p.id, p.name
FROM market.products p
LEFT JOIN market.product_images pi ON pi.product_id = p.id
WHERE pi.id IS NULL
   OR pi.image_url LIKE '%placeholder%'
LIMIT 50;
```

### Товары с изображениями
```sql
SELECT 
    p.id,
    p.name,
    COUNT(pi.id) as images_count,
    STRING_AGG(pi.image_url, ', ') as image_urls
FROM market.products p
LEFT JOIN market.product_images pi ON pi.product_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(pi.id) > 0
LIMIT 20;
```

### Изображения по категориям
```sql
SELECT 
    c.name as category,
    COUNT(DISTINCT p.id) as products,
    COUNT(pi.id) as images,
    COUNT(CASE WHEN pi.image_url LIKE '%placeholder%' THEN 1 END) as with_placeholder
FROM market.categories c
LEFT JOIN market.products p ON p.category_id = c.id
LEFT JOIN market.product_images pi ON pi.product_id = p.id
GROUP BY c.id, c.name
ORDER BY products DESC;
```

---

## 🎯 URL изображений на фронте

### Оригинал:
```
/uploads/products/original/filename.jpg
```

### Миниатюра (автогенерация):
```
/uploads/products/thumbnails/filename.jpg
```

### Оптимизированное (автогенерация):
```
/uploads/products/optimized/filename.jpg
```

### Плейсхолдер:
```
/uploads/products/placeholder.jpg
```

---

## 💡 Рекомендации

### 1. Приоритет корректировки
1. Сначала назначьте изображения популярным товарам
2. Затем товарам с высоким рейтингом
3. Остальные можно оставить с плейсхолдером

### 2. Пакетная обработка
Обрабатывайте по 50-100 товаров за раз:
```sql
-- Выбрать следующие 50 товаров без изображений
SELECT id, name 
FROM market.products p
WHERE NOT EXISTS (
    SELECT 1 FROM market.product_images pi 
    WHERE pi.product_id = p.id 
      AND pi.image_url NOT LIKE '%placeholder%'
)
LIMIT 50;
```

### 3. Резервное копирование
Перед массовыми изменениями:
```sql
-- Создать резервную копию
CREATE TABLE temp.product_images_backup AS 
SELECT * FROM market.product_images;
```

---

## 📝 Пример workflow

```sql
-- 1. Найти товар
SELECT id, name FROM market.products WHERE name LIKE '%молоко%' LIMIT 5;
-- Результат: id=100, name='Молоко коровье'

-- 2. Найти подходящее изображение
SELECT old_file_id, old_filename 
FROM temp.image_mapping 
WHERE old_filename LIKE '%milk%' OR old_filename LIKE '%moloko%'
LIMIT 5;
-- Результат: old_file_id=200, old_filename='milk_fresh.jpg'

-- 3. Назначить изображение
UPDATE market.product_images 
SET image_url = '/uploads/products/original/milk_fresh.jpg',
    old_id = 200
WHERE product_id = 100;

-- 4. Отметить в маппинге
UPDATE temp.image_mapping
SET new_product_id = 100,
    new_image_id = (SELECT id FROM market.product_images WHERE product_id = 100),
    is_correct = TRUE,
    notes = 'Молоко - назначено вручную'
WHERE old_file_id = 200;

-- 5. Проверить
SELECT p.name, pi.image_url, pi.old_id
FROM market.products p
JOIN market.product_images pi ON pi.product_id = p.id
WHERE p.id = 100;
```

---

## ✅ Чек-лист

- [ ] Запустить `setup_images.py`
- [ ] Скопировать файлы в `uploads/products/original/`
- [ ] Запустить миграцию
- [ ] Проверить статистику
- [ ] Начать ручную корректировку
- [ ] Отслеживать прогресс через `temp.image_mapping`

---

**Готово к работе!** 🖼️

Изображения будут с плейсхолдерами, но у вас есть:
- ✅ Поле `old_id` для отслеживания
- ✅ Таблица `temp.image_mapping` для работы
- ✅ SQL примеры для корректировки
- ✅ Возможность постепенно исправлять
