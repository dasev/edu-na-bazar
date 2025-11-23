-- Пересоздание всех таблиц с BIGSERIAL для id

-- Удаляем все таблицы
DROP TABLE IF EXISTS store_owners CASCADE;
DROP TABLE IF EXISTS cart_items CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Удаляем типы
DROP TYPE IF EXISTS store_status CASCADE;

-- Таблица users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    avatar TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Таблица categories
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    image TEXT,
    parent_id BIGINT REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Таблица products
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price DOUBLE PRECISION NOT NULL,
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    image TEXT,
    in_stock BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Таблица cart_items
CREATE TABLE cart_items (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

-- Таблица store_owners
CREATE TABLE store_owners (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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

-- Индексы
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_cart_items_user_id ON cart_items(user_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);
CREATE INDEX idx_store_owners_owner_id ON store_owners(owner_id);
CREATE INDEX idx_store_owners_inn ON store_owners(inn);
CREATE INDEX idx_store_owners_status ON store_owners(status);
