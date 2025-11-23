-- Добавление поля unit в products

ALTER TABLE market.products 
ADD COLUMN IF NOT EXISTS unit TEXT DEFAULT 'шт';
