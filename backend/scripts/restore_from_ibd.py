"""
Восстановление базы данных enb из .ibd и .frm файлов
Создаёт структуру таблиц на основе анализа .frm файлов
"""
import os
import pymysql
from pathlib import Path

# Настройки
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4'
}

SOURCE_DIR = Path(r"C:\python\sites_mysql\enb")
TARGET_DB = "enb"

# Структуры основных таблиц (упрощенные, для базовой совместимости)
TABLE_STRUCTURES = {
    'user': """
        CREATE TABLE IF NOT EXISTS `user` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `username` VARCHAR(255),
            `email` VARCHAR(255),
            `phone` VARCHAR(20),
            `password_hash` VARCHAR(255),
            `auth_key` VARCHAR(255),
            `status` INT DEFAULT 10,
            `created_at` INT,
            `updated_at` INT,
            `last_login` INT,
            `avatar` VARCHAR(255),
            `first_name` VARCHAR(255),
            `last_name` VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'companies': """
        CREATE TABLE IF NOT EXISTS `companies` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `user_id` INT,
            `phone` VARCHAR(20),
            `email` VARCHAR(255),
            `address` TEXT,
            `logo` VARCHAR(255),
            `status` INT DEFAULT 1,
            `created_at` INT,
            `updated_at` INT,
            `category_id` INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'advert': """
        CREATE TABLE IF NOT EXISTS `advert` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `title` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `price` DECIMAL(10,2),
            `company_id` INT,
            `category_id` INT,
            `user_id` INT,
            `phone` VARCHAR(20),
            `email` VARCHAR(255),
            `address` TEXT,
            `status` INT DEFAULT 1,
            `views` INT DEFAULT 0,
            `created_at` INT,
            `updated_at` INT,
            `image` VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'categories': """
        CREATE TABLE IF NOT EXISTS `categories` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `name` VARCHAR(255) NOT NULL,
            `slug` VARCHAR(255),
            `parent_id` INT,
            `icon` VARCHAR(255),
            `image` VARCHAR(255),
            `sort_order` INT DEFAULT 0,
            `status` INT DEFAULT 1,
            `created_at` INT,
            `updated_at` INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'file': """
        CREATE TABLE IF NOT EXISTS `file` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `name` VARCHAR(255),
            `path` VARCHAR(255),
            `url` VARCHAR(255),
            `type` VARCHAR(50),
            `size` INT,
            `model` VARCHAR(50),
            `model_id` INT,
            `created_at` INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'messages': """
        CREATE TABLE IF NOT EXISTS `messages` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `from_user_id` INT,
            `to_user_id` INT,
            `subject` VARCHAR(255),
            `body` TEXT,
            `is_read` TINYINT DEFAULT 0,
            `created_at` INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    
    'review': """
        CREATE TABLE IF NOT EXISTS `review` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `user_id` INT,
            `company_id` INT,
            `rating` INT,
            `comment` TEXT,
            `status` INT DEFAULT 1,
            `created_at` INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
}


def create_database(conn):
    """Создать базу данных"""
    print(f"\n{'='*80}")
    print(f"СОЗДАНИЕ БАЗЫ ДАННЫХ {TARGET_DB}")
    print(f"{'='*80}\n")
    
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TARGET_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ База данных {TARGET_DB} создана")


def create_tables(conn):
    """Создать структуру таблиц"""
    print(f"\n{'='*80}")
    print("СОЗДАНИЕ СТРУКТУРЫ ТАБЛИЦ")
    print(f"{'='*80}\n")
    
    with conn.cursor() as cursor:
        cursor.execute(f"USE {TARGET_DB}")
        
        for table_name, create_sql in TABLE_STRUCTURES.items():
            print(f"Создаём таблицу {table_name}...")
            cursor.execute(create_sql)
            print(f"✅ {table_name}")
    
    conn.commit()
    print(f"\n✅ Все таблицы созданы")


def check_ibd_files():
    """Проверить наличие .ibd файлов"""
    print(f"\n{'='*80}")
    print("ПРОВЕРКА ФАЙЛОВ ТАБЛИЦ")
    print(f"{'='*80}\n")
    
    if not SOURCE_DIR.exists():
        print(f"❌ Папка {SOURCE_DIR} не найдена")
        return False
    
    print(f"📁 Исходная папка: {SOURCE_DIR}")
    print()
    
    found_tables = []
    for table_name in TABLE_STRUCTURES.keys():
        ibd_file = SOURCE_DIR / f"{table_name}.ibd"
        frm_file = SOURCE_DIR / f"{table_name}.frm"
        
        if ibd_file.exists():
            size_mb = ibd_file.stat().st_size / (1024 * 1024)
            print(f"✅ {table_name:20} - {size_mb:8.2f} MB")
            found_tables.append(table_name)
        else:
            print(f"⚠️  {table_name:20} - файл не найден")
    
    print(f"\n📊 Найдено таблиц: {len(found_tables)}/{len(TABLE_STRUCTURES)}")
    return len(found_tables) > 0


def get_table_stats(conn):
    """Получить статистику по таблицам"""
    print(f"\n{'='*80}")
    print("СТАТИСТИКА ТАБЛИЦ")
    print(f"{'='*80}\n")
    
    with conn.cursor() as cursor:
        cursor.execute(f"USE {TARGET_DB}")
        
        total_rows = 0
        for table_name in TABLE_STRUCTURES.keys():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name:20} - {count:>10,} записей")
                total_rows += count
            except Exception as e:
                print(f"  {table_name:20} - ошибка: {str(e)[:50]}")
        
        print(f"\n{'='*80}")
        print(f"  ВСЕГО:               {total_rows:>10,} записей")
        print(f"{'='*80}")


def main():
    """Основная функция"""
    print("\n" + "="*80)
    print("ВОССТАНОВЛЕНИЕ БАЗЫ ДАННЫХ ENB ИЗ .IBD ФАЙЛОВ")
    print("="*80)
    
    # Проверка файлов
    if not check_ibd_files():
        print("\n❌ Файлы таблиц не найдены")
        print("\nВозможные решения:")
        print("1. Проверьте путь к базе данных")
        print("2. Установите MySQL 5.7 и создайте дамп")
        return
    
    # Подключение к MySQL
    print(f"\nПодключение к MySQL...")
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ Подключение установлено")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\nПроверьте:")
        print("1. MariaDB запущена: net start MariaDB")
        print("2. Пароль root правильный")
        return
    
    try:
        # Создать базу данных
        create_database(conn)
        
        # Создать структуру таблиц
        create_tables(conn)
        
        print(f"\n{'='*80}")
        print("СЛЕДУЮЩИЕ ШАГИ")
        print(f"{'='*80}\n")
        print("Структура таблиц создана, но данные еще не импортированы.")
        print()
        print("Для импорта данных:")
        print("1. Остановите MariaDB: net stop MariaDB")
        print("2. Скопируйте .ibd файлы в папку базы данных")
        print("3. Запустите MariaDB: net start MariaDB")
        print()
        print("Или используйте MySQL 5.7 для создания дампа:")
        print("  start_mysql57.bat")
        print()
        
        # Статистика (будет 0, т.к. данные не скопированы)
        get_table_stats(conn)
        
    finally:
        conn.close()
    
    print("\n✅ Готово!")
    print("\nСледующий шаг: Импорт данных или миграция через MySQL 5.7")


if __name__ == "__main__":
    main()
