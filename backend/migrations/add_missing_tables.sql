-- Добавление недостающих таблиц

-- Таблица sms_codes
CREATE TABLE IF NOT EXISTS config.sms_codes (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    code TEXT NOT NULL,
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    attempts TEXT NOT NULL DEFAULT '0',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_config_sms_codes_phone ON config.sms_codes(phone);

-- Таблица orders
CREATE TABLE IF NOT EXISTS market.orders (
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

CREATE INDEX IF NOT EXISTS idx_market_orders_user_id ON market.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_market_orders_status ON market.orders(status);

-- Таблица order_items
CREATE TABLE IF NOT EXISTS market.order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES market.orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    quantity BIGINT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_market_order_items_order_id ON market.order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_market_order_items_product_id ON market.order_items(product_id);

-- Таблица stores
CREATE TABLE IF NOT EXISTS market.stores (
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
