-- Проверка данных в схеме temp

-- 1. Список всех таблиц в схеме temp
SELECT schemaname, tablename 
FROM pg_tables 
WHERE schemaname = 'temp'
ORDER BY tablename;

-- 2. Количество записей в каждой таблице
SELECT 
    'temp.seller' as table_name, 
    COUNT(*) as count 
FROM temp.seller
UNION ALL
SELECT 'temp.categories', COUNT(*) FROM temp.categories
UNION ALL
SELECT 'temp.companies', COUNT(*) FROM temp.companies
UNION ALL
SELECT 'temp.sub_categories', COUNT(*) FROM temp.sub_categories
UNION ALL
SELECT 'temp.user', COUNT(*) FROM temp.user
UNION ALL
SELECT 'temp.review', COUNT(*) FROM temp.review
UNION ALL
SELECT 'temp.file', COUNT(*) FROM temp.file
UNION ALL
SELECT 'temp.advert', COUNT(*) FROM temp.advert
ORDER BY table_name;

-- 3. Примеры данных из каждой таблицы

-- Категории
SELECT 'CATEGORIES' as table_name, * FROM temp.categories LIMIT 5;

-- Компании
SELECT 'COMPANIES' as table_name, * FROM temp.companies LIMIT 5;

-- Подкатегории
SELECT 'SUB_CATEGORIES' as table_name, * FROM temp.sub_categories LIMIT 5;

-- Пользователи
SELECT 'USERS' as table_name, * FROM temp.user LIMIT 5;

-- Файлы
SELECT 'FILES' as table_name, * FROM temp.file LIMIT 5;

-- Продавцы
SELECT 'SELLERS' as table_name, * FROM temp.seller LIMIT 5;
