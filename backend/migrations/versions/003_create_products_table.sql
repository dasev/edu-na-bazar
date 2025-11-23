-- Create products table
-- Migration: 003_create_products_table

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    old_price NUMERIC(10, 2),
    image VARCHAR(500),
    images TEXT[],
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    rating NUMERIC(3, 2) DEFAULT 0.0,
    reviews_count INTEGER DEFAULT 0,
    in_stock BOOLEAN DEFAULT TRUE,
    stock_quantity INTEGER DEFAULT 0,
    unit VARCHAR(50) DEFAULT 'шт',
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_rating ON products(rating);
CREATE INDEX idx_products_created_at ON products(created_at);
CREATE INDEX idx_products_in_stock ON products(in_stock);

-- Full-text search index
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);

-- Comments
COMMENT ON TABLE products IS 'Товары';
COMMENT ON COLUMN products.slug IS 'URL-friendly название';
COMMENT ON COLUMN products.old_price IS 'Старая цена для отображения скидки';
COMMENT ON COLUMN products.images IS 'Массив URL дополнительных изображений';
COMMENT ON COLUMN products.rating IS 'Рейтинг от 0.00 до 5.00';
COMMENT ON COLUMN products.unit IS 'Единица измерения: шт, кг, л, упак';
