-- Создание таблицы store_owners для магазинов пользователей

-- Удаляем таблицу если существует
DROP TABLE IF EXISTS store_owners CASCADE;

-- Удаляем тип если существует и создаем заново
DROP TYPE IF EXISTS store_status CASCADE;
CREATE TYPE store_status AS ENUM ('pending', 'active', 'suspended', 'rejected');

CREATE TABLE store_owners (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    inn VARCHAR(12) NOT NULL UNIQUE,
    kpp VARCHAR(9),
    ogrn VARCHAR(15),
    name VARCHAR(500) NOT NULL,
    legal_name VARCHAR(1000) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    description TEXT,
    logo VARCHAR(500),
    banner VARCHAR(500),
    status store_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_store_owners_owner_id ON store_owners(owner_id);
CREATE INDEX IF NOT EXISTS idx_store_owners_inn ON store_owners(inn);
CREATE INDEX IF NOT EXISTS idx_store_owners_status ON store_owners(status);

-- Комментарии
COMMENT ON TABLE store_owners IS 'Магазины пользователей';
COMMENT ON COLUMN store_owners.id IS 'ID магазина';
COMMENT ON COLUMN store_owners.owner_id IS 'ID владельца';
COMMENT ON COLUMN store_owners.inn IS 'ИНН организации';
COMMENT ON COLUMN store_owners.kpp IS 'КПП';
COMMENT ON COLUMN store_owners.ogrn IS 'ОГРН';
COMMENT ON COLUMN store_owners.name IS 'Название магазина';
COMMENT ON COLUMN store_owners.legal_name IS 'Юридическое название';
COMMENT ON COLUMN store_owners.address IS 'Адрес';
COMMENT ON COLUMN store_owners.phone IS 'Телефон';
COMMENT ON COLUMN store_owners.email IS 'Email';
COMMENT ON COLUMN store_owners.description IS 'Описание';
COMMENT ON COLUMN store_owners.logo IS 'URL логотипа';
COMMENT ON COLUMN store_owners.banner IS 'URL баннера';
COMMENT ON COLUMN store_owners.status IS 'Статус магазина';
COMMENT ON COLUMN store_owners.created_at IS 'Дата создания';
COMMENT ON COLUMN store_owners.updated_at IS 'Дата обновления';
