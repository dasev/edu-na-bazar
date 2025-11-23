-- Добавление поля address в таблицу users
-- Миграция: 008_add_address_to_users.sql

-- Добавляем колонку address
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS address VARCHAR(500);

-- Комментарий
COMMENT ON COLUMN users.address IS 'Адрес доставки пользователя';

-- Проверка
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'address';
