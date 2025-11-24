-- Добавление полей icon, slug, sort_order в таблицу categories
-- Безопасно: только ADD COLUMN, никаких удалений!

-- Добавляем колонку icon (emoji иконка)
ALTER TABLE market.categories 
ADD COLUMN IF NOT EXISTS icon TEXT;

-- Добавляем колонку slug (URL-friendly название)
ALTER TABLE market.categories 
ADD COLUMN IF NOT EXISTS slug TEXT;

-- Добавляем индекс на slug
CREATE INDEX IF NOT EXISTS idx_categories_slug ON market.categories(slug);

-- Добавляем колонку sort_order (порядок сортировки)
ALTER TABLE market.categories 
ADD COLUMN IF NOT EXISTS sort_order BIGINT DEFAULT 0;

-- Проверяем структуру таблицы
\d market.categories
