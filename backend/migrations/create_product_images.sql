-- Создание таблицы для изображений товаров

CREATE TABLE IF NOT EXISTS market.product_images (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES market.products(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_images_product_id ON market.product_images(product_id);
CREATE INDEX IF NOT EXISTS idx_product_images_sort_order ON market.product_images(product_id, sort_order);
