-- Добавление полей rating и reviews_count в products

ALTER TABLE market.products 
ADD COLUMN IF NOT EXISTS rating DOUBLE PRECISION DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS reviews_count BIGINT DEFAULT 0;

-- Проверка
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_schema = 'market' 
  AND table_name = 'products'
ORDER BY ordinal_position;
