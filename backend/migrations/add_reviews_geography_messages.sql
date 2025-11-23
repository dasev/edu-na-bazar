-- Добавление таблиц: отзывы, география, сообщения

-- 1. Создаем схему для географии
CREATE SCHEMA IF NOT EXISTS geo;

-- 2. Таблица регионов
CREATE TABLE IF NOT EXISTS geo.regions (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_regions_code ON geo.regions(code);
CREATE INDEX IF NOT EXISTS idx_regions_name ON geo.regions(name);

-- 3. Таблица городов
CREATE TABLE IF NOT EXISTS geo.cities (
    id BIGSERIAL PRIMARY KEY,
    region_id BIGINT REFERENCES geo.regions(id),
    name TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cities_region ON geo.cities(region_id);
CREATE INDEX IF NOT EXISTS idx_cities_name ON geo.cities(name);
CREATE INDEX IF NOT EXISTS idx_cities_location ON geo.cities(latitude, longitude);

-- 4. Таблица отзывов
CREATE TABLE IF NOT EXISTS market.reviews (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES market.products(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES config.users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reviews_product ON market.reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user ON market.reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON market.reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_approved ON market.reviews(is_approved);
CREATE INDEX IF NOT EXISTS idx_reviews_created ON market.reviews(created_at DESC);

-- 5. Таблица сообщений
CREATE TABLE IF NOT EXISTS market.messages (
    id BIGSERIAL PRIMARY KEY,
    from_user_id BIGINT REFERENCES config.users(id) ON DELETE CASCADE,
    to_user_id BIGINT REFERENCES config.users(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES market.products(id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_from ON market.messages(from_user_id);
CREATE INDEX IF NOT EXISTS idx_messages_to ON market.messages(to_user_id);
CREATE INDEX IF NOT EXISTS idx_messages_product ON market.messages(product_id);
CREATE INDEX IF NOT EXISTS idx_messages_is_read ON market.messages(is_read);
CREATE INDEX IF NOT EXISTS idx_messages_created ON market.messages(created_at DESC);

-- 6. Добавляем комментарии
COMMENT ON TABLE geo.regions IS 'Регионы РФ';
COMMENT ON TABLE geo.cities IS 'Города РФ';
COMMENT ON TABLE market.reviews IS 'Отзывы на товары';
COMMENT ON TABLE market.messages IS 'Личные сообщения между пользователями';

COMMENT ON COLUMN market.reviews.is_approved IS 'Отзыв прошел модерацию';
COMMENT ON COLUMN market.messages.product_id IS 'Товар о котором идет речь (опционально)';
