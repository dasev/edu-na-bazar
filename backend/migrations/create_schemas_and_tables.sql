-- Создание схем и таблиц с BIGSERIAL

-- Создаем схемы
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS market;

-- ============================================
-- СХЕМА CONFIG - пользователи и настройки
-- ============================================

-- Таблица users
CREATE TABLE config.users (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    address TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_config_users_email ON config.users(email);
CREATE INDEX idx_config_users_phone ON config.users(phone);

-- ============================================
-- СХЕМА MARKET - бизнес-данные
-- ============================================

-- Таблица categories
CREATE TABLE market.categories (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    image TEXT,
    parent_id BIGINT REFERENCES market.categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_categories_parent_id ON market.categories(parent_id);

-- Таблица products
CREATE TABLE market.products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price DOUBLE PRECISION NOT NULL,
    category_id BIGINT REFERENCES market.categories(id) ON DELETE SET NULL,
    image TEXT,
    in_stock BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_products_category_id ON market.products(category_id);

-- Таблица cart_items
CREATE TABLE market.cart_items (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    quantity BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

CREATE INDEX idx_market_cart_items_user_id ON market.cart_items(user_id);
CREATE INDEX idx_market_cart_items_product_id ON market.cart_items(product_id);

-- Таблица store_owners
CREATE TABLE market.store_owners (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    inn TEXT NOT NULL UNIQUE,
    kpp TEXT,
    ogrn TEXT,
    name TEXT NOT NULL,
    legal_name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    description TEXT,
    logo TEXT,
    banner TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_store_owners_owner_id ON market.store_owners(owner_id);
CREATE INDEX idx_market_store_owners_inn ON market.store_owners(inn);
CREATE INDEX idx_market_store_owners_status ON market.store_owners(status);

-- Таблица sms_codes
CREATE TABLE config.sms_codes (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    code TEXT NOT NULL,
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    attempts TEXT NOT NULL DEFAULT '0',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP
);

CREATE INDEX idx_config_sms_codes_phone ON config.sms_codes(phone);

-- Таблица orders
CREATE TABLE market.orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    store_id BIGINT,
    total_amount DOUBLE PRECISION NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    delivery_phone TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_orders_user_id ON market.orders(user_id);
CREATE INDEX idx_market_orders_status ON market.orders(status);

-- Таблица order_items
CREATE TABLE market.order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES market.orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    quantity BIGINT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_order_items_order_id ON market.order_items(order_id);
CREATE INDEX idx_market_order_items_product_id ON market.order_items(product_id);

-- Таблица stores
CREATE TABLE market.stores (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    phone TEXT,
    email TEXT,
    logo TEXT,
    banner TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии
COMMENT ON SCHEMA config IS 'Конфигурация: пользователи и настройки';
COMMENT ON SCHEMA market IS 'Маркетплейс: товары, магазины, корзины';
