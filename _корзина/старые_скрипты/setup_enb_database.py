"""
Настройка базы данных enb в MariaDB
Копирование файлов из старой директории
"""
import pymysql
import shutil
import os

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4',
}

OLD_DATA_DIR = r"C:\python\sites_mysql\enb"

def find_mariadb_datadir():
    """Найти директорию данных MariaDB"""
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT @@datadir")
        datadir = cursor.fetchone()[0]
        conn.close()
        return datadir.rstrip('\\').rstrip('/')
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def main():
    print("="*80)
    print("🔧 НАСТРОЙКА БАЗЫ ДАННЫХ ENB")
    print("="*80)
    
    # Находим datadir
    datadir = find_mariadb_datadir()
    if not datadir:
        print("❌ Не удалось найти директорию данных MariaDB")
        return
    
    print(f"📁 MariaDB datadir: {datadir}")
    print(f"📁 Старые данные: {OLD_DATA_DIR}")
    
    # Создаем базу данных
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        print("\n📦 Создание базы данных enb...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ База данных создана")
        
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    # Копируем файлы
    target_dir = os.path.join(datadir, 'enb')
    
    print(f"\n📋 Инструкция по копированию файлов:")
    print("="*80)
    print("1. Остановите службу MariaDB:")
    print("   net stop MariaDB")
    print()
    print("2. Скопируйте файлы:")
    print(f"   xcopy \"{OLD_DATA_DIR}\" \"{target_dir}\" /E /I /Y")
    print()
    print("3. Запустите службу MariaDB:")
    print("   net start MariaDB")
    print()
    print("4. Проверьте таблицы:")
    print("   mysql -u root -proot enb -e \"SHOW TABLES;\"")
    print("="*80)
    
    print("\n⚠️  ВНИМАНИЕ: Нужны права администратора!")
    print("Запустите PowerShell/CMD от имени администратора")

if __name__ == "__main__":
    main()
