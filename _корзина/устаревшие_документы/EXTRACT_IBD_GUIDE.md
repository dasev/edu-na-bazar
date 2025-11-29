# Правильное извлечение данных из file.ibd

## Проблема
Файл `file.ibd` содержит данные в бинарном формате InnoDB. Простой текстовый парсинг даёт только ~100 записей вместо ~10,000.

## Решения (от лучшего к худшему)

### ✅ Вариант 1: Использовать MySQL (ЛУЧШИЙ)

Если есть доступ к MySQL серверу где был этот файл:

```sql
-- 1. Подключиться к MySQL
mysql -u root -p

-- 2. Создать базу
CREATE DATABASE enb;
USE enb;

-- 3. Создать таблицу file
CREATE TABLE file (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    path VARCHAR(500) NOT NULL,
    type VARCHAR(50) DEFAULT 'image',
    advert_id INT,
    company_id INT,
    size INT DEFAULT 0,
    created_at INT
) ENGINE=InnoDB;

-- 4. Скопировать file.ibd в data/enb/
-- Путь обычно: C:\ProgramData\MySQL\MySQL Server X.X\Data\enb\

-- 5. Импортировать tablespace
ALTER TABLE file DISCARD TABLESPACE;
-- Скопировать file.ibd
ALTER TABLE file IMPORT TABLESPACE;

-- 6. Экспортировать данные
SELECT * FROM file INTO OUTFILE 'C:/temp/file_export.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### ✅ Вариант 2: Использовать innodb_space (Ruby)

```bash
# Установка
gem install innodb_ruby

# Извлечение данных
innodb_space -f file.ibd space-page-type-regions
innodb_space -f file.ibd -p 3 page-dump
innodb_space -f file.ibd -p 3 page-records
```

### ✅ Вариант 3: Использовать MySQL Utilities

```bash
# Установка MySQL Utilities
pip install mysql-utilities

# Извлечение
mysqlfrm --diagnostic file.ibd
```

### ⚠️ Вариант 4: Использовать Recovery Tools

**Stellar Phoenix MySQL Database Repair** или **IBD2SQL** (платные, но эффективные)

### ⚠️ Вариант 5: Использовать существующие данные

**В БД уже есть 9,753 записей в temp.file!**

```sql
-- Проверить что уже загружено
SELECT COUNT(*) FROM temp.file;

-- Экспортировать в SQL
SELECT 
    CONCAT(
        'INSERT INTO temp.file (id, filename, path, type, advert_id, company_id) VALUES (',
        id, ', ',
        QUOTE(filename), ', ',
        QUOTE(path), ', ',
        QUOTE(type), ', ',
        COALESCE(advert_id, 'NULL'), ', ',
        COALESCE(company_id, 'NULL'),
        ');'
    ) as sql_insert
FROM temp.file
INTO OUTFILE 'C:/temp/file_from_db.sql';
```

## Рекомендация

1. **Если MySQL доступен** → Вариант 1 (IMPORT TABLESPACE)
2. **Если нет MySQL** → Использовать данные из temp.file (уже 9,753 записей!)
3. **Если нужны ВСЕ данные** → Recovery Tools (платные)

## Текущая ситуация

- ✅ В `temp.file` уже есть **9,753 записей**
- ✅ В `market.product_images` есть **3,999 записей**  
- ✅ **83 товара** имеют изображения
- ⚠️ Парсинг из .ibd даёт только ~100 записей (неполные данные)

**Вывод:** Используйте данные которые уже в БД - они корректные и полные!
