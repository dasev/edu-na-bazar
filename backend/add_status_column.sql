-- Добавляем колонку status в таблицу store_owners

ALTER TABLE store_owners 
ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'pending';

-- Создаем индекс
CREATE INDEX IF NOT EXISTS idx_store_owners_status ON store_owners(status);
