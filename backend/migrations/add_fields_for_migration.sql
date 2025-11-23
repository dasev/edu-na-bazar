-- Добавление полей для миграции из старой базы enb

-- 1. Добавляем поля в market.products
ALTER TABLE market.products 
ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS location TEXT,
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active';

COMMENT ON COLUMN market.products.views IS 'Количество просмотров товара';
COMMENT ON COLUMN market.products.location IS 'Адрес/местоположение товара';
COMMENT ON COLUMN market.products.status IS 'Статус товара: active, archived, moderation';

-- 2. Добавляем поля в market.store_owners
ALTER TABLE market.store_owners 
ADD COLUMN IF NOT EXISTS category_id BIGINT REFERENCES market.categories(id),
ADD COLUMN IF NOT EXISTS inn TEXT,
ADD COLUMN IF NOT EXISTS ogrn TEXT,
ADD COLUMN IF NOT EXISTS working_hours TEXT,
ADD COLUMN IF NOT EXISTS website TEXT;

COMMENT ON COLUMN market.store_owners.category_id IS 'Категория магазина';
COMMENT ON COLUMN market.store_owners.inn IS 'ИНН организации';
COMMENT ON COLUMN market.store_owners.ogrn IS 'ОГРН организации';
COMMENT ON COLUMN market.store_owners.working_hours IS 'Часы работы магазина';
COMMENT ON COLUMN market.store_owners.website IS 'Сайт магазина';

-- 3. Добавляем поля в auth.users
ALTER TABLE auth.users 
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP,
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active';

COMMENT ON COLUMN auth.users.last_login IS 'Дата последнего входа';
COMMENT ON COLUMN auth.users.status IS 'Статус пользователя: active, blocked';

-- 4. Создаем индексы для новых полей
CREATE INDEX IF NOT EXISTS idx_products_status ON market.products(status);
CREATE INDEX IF NOT EXISTS idx_products_views ON market.products(views DESC);
CREATE INDEX IF NOT EXISTS idx_store_owners_category ON market.store_owners(category_id);
CREATE INDEX IF NOT EXISTS idx_users_status ON auth.users(status);
CREATE INDEX IF NOT EXISTS idx_users_last_login ON auth.users(last_login DESC);

-- 5. Обновляем существующие записи (если есть)
UPDATE market.products SET status = 'active' WHERE status IS NULL;
UPDATE auth.users SET status = 'active' WHERE status IS NULL;
