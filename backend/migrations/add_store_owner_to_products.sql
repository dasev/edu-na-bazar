-- Добавление поля store_owner_id в products

ALTER TABLE market.products 
ADD COLUMN IF NOT EXISTS store_owner_id BIGINT REFERENCES market.store_owners(id);

CREATE INDEX IF NOT EXISTS idx_products_store_owner_id ON market.products(store_owner_id);
