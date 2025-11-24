-- Обновление иконок для существующих категорий и добавление новых
-- НЕ УДАЛЯЕТ существующие данные!

-- Обновляем иконки для существующих категорий
UPDATE market.categories SET icon = '🌱' WHERE name LIKE '%гротовар%' OR name LIKE '%удобрени%';
UPDATE market.categories SET icon = '🥫' WHERE name LIKE '%отов%' AND name LIKE '%продукт%';
UPDATE market.categories SET icon = '🌾' WHERE name LIKE '%ерн%';
UPDATE market.categories SET icon = '🌽' WHERE name LIKE '%орм%' OR name LIKE '%добав%';
UPDATE market.categories SET icon = '🍯' WHERE name LIKE '%ед%';
UPDATE market.categories SET icon = '🥛' WHERE name LIKE '%олочн%';
UPDATE market.categories SET icon = '🥩' WHERE name LIKE '%ясо%' OR name LIKE '%птиц%' OR name LIKE '%рыб%';
UPDATE market.categories SET icon = '🚜' WHERE name LIKE '%борудован%' OR name LIKE '%техник%';
UPDATE market.categories SET icon = '🥬' WHERE name LIKE '%вощ%' OR name LIKE '%рукт%';
UPDATE market.categories SET icon = '⚙️' WHERE name LIKE '%слуг%';

-- Добавляем новые категории если их нет
INSERT INTO market.categories (name, slug, icon, sort_order, created_at, updated_at)
SELECT 'Яйца', 'eggs', '🥚', 11, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM market.categories WHERE slug = 'eggs');

INSERT INTO market.categories (name, slug, icon, sort_order, created_at, updated_at)
SELECT 'Саженцы и семена', 'seedlings', '🌿', 12, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM market.categories WHERE slug = 'seedlings');

-- Проверяем результат
SELECT id, name, icon, slug, sort_order 
FROM market.categories 
ORDER BY sort_order;
