-- Копирование данных из public в config/market

-- Копируем users из public в config
INSERT INTO config.users (id, email, phone, full_name, address, is_active, is_verified, created_at, updated_at, last_login)
SELECT 
    nextval('config.users_id_seq'),
    email,
    phone,
    full_name,
    address,
    is_active,
    is_verified,
    created_at,
    updated_at,
    last_login
FROM public.users
ON CONFLICT DO NOTHING;

-- Копируем categories из public в market
INSERT INTO market.categories (id, name, description, image, parent_id, created_at, updated_at)
SELECT 
    nextval('market.categories_id_seq'),
    name,
    description,
    image,
    NULL, -- parent_id пока NULL, т.к. UUID не совпадают
    created_at,
    updated_at
FROM public.categories
ON CONFLICT DO NOTHING;

-- Копируем products из public в market
INSERT INTO market.products (id, name, description, price, category_id, image, in_stock, created_at, updated_at)
SELECT 
    nextval('market.products_id_seq'),
    name,
    description,
    price::double precision,
    NULL, -- category_id пока NULL
    image,
    in_stock,
    created_at,
    updated_at
FROM public.products
ON CONFLICT DO NOTHING;

-- Выводим статистику
SELECT 'config.users' as table_name, COUNT(*) as count FROM config.users
UNION ALL
SELECT 'market.categories', COUNT(*) FROM market.categories
UNION ALL
SELECT 'market.products', COUNT(*) FROM market.products;
