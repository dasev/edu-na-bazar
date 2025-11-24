-- Добавление геолокации для товаров
-- Дата: 2025-11-25

-- Добавляем колонки для геолокации
ALTER TABLE market.products 
ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS geo_location GEOMETRY(POINT, 4326);

-- Создаем индекс для geo_location (PostGIS GIST индекс)
CREATE INDEX IF NOT EXISTS idx_products_geo_location 
ON market.products USING GIST (geo_location);

-- Создаем индексы для latitude и longitude
CREATE INDEX IF NOT EXISTS idx_products_latitude 
ON market.products (latitude);

CREATE INDEX IF NOT EXISTS idx_products_longitude 
ON market.products (longitude);

-- Комментарии
COMMENT ON COLUMN market.products.latitude IS 'Широта местоположения товара';
COMMENT ON COLUMN market.products.longitude IS 'Долгота местоположения товара';
COMMENT ON COLUMN market.products.geo_location IS 'Геометрическая точка для PostGIS запросов';
