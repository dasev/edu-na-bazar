"""
Восстановление одной таблицы из .ibd файла в чистый MySQL 5.7
"""
import subprocess
import time
import os
import shutil
from pathlib import Path

MYSQL57_BIN = Path("C:/mysql57/bin")
SOURCE_DIR = Path("C:/python/sites_mysql/enb")
NEW_DATA_DIR = Path("C:/mysql57_data")
TABLE_NAME = "companies"

def run_mysql_command(sql, wait_for_server=False):
    """Выполнить SQL команду"""
    if wait_for_server:
        time.sleep(2)
    
    cmd = [
        str(MYSQL57_BIN / "mysql.exe"),
        "-u", "root",
        "--protocol=TCP",
        "--port=3306",
        "-e", sql
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def main():
    print("\n" + "="*80)
    print("ВОССТАНОВЛЕНИЕ ТАБЛИЦЫ COMPANIES")
    print("="*80 + "\n")
    
    # Проверка файлов
    ibd_file = SOURCE_DIR / f"{TABLE_NAME}.ibd"
    frm_file = SOURCE_DIR / f"{TABLE_NAME}.frm"
    
    if not ibd_file.exists():
        print(f"❌ Файл {ibd_file} не найден")
        return
    
    print(f"✅ Файлы найдены:")
    print(f"   {TABLE_NAME}.ibd - {ibd_file.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"   {TABLE_NAME}.frm - {frm_file.stat().st_size} bytes")
    print()
    
    # Проверка что MySQL 5.7 запущен
    print("Проверка подключения к MySQL 5.7...")
    success, stdout, stderr = run_mysql_command("SELECT VERSION();", wait_for_server=True)
    
    if not success:
        print("❌ MySQL 5.7 не запущен или недоступен")
        print("\nЗапустите MySQL 5.7 в отдельном окне:")
        print(f"  cd {MYSQL57_BIN}")
        print(f"  .\\mysqld.exe --datadir={NEW_DATA_DIR} --console")
        print("\nЗатем запустите этот скрипт снова")
        return
    
    print("✅ MySQL 5.7 доступен")
    print()
    
    # Создание базы данных
    print("Создание базы данных enb...")
    run_mysql_command("CREATE DATABASE IF NOT EXISTS enb;")
    print("✅ База создана")
    print()
    
    # Создание структуры таблицы
    print(f"Создание структуры таблицы {TABLE_NAME}...")
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS enb.{TABLE_NAME} (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        description TEXT,
        user_id INT,
        phone VARCHAR(20),
        email VARCHAR(255),
        address TEXT,
        logo VARCHAR(255),
        status INT,
        created_at INT,
        updated_at INT,
        category_id INT
    ) ENGINE=InnoDB ROW_FORMAT=COMPACT;
    """
    run_mysql_command(create_table_sql)
    print("✅ Структура создана")
    print()
    
    # Отключение tablespace
    print("Отключение tablespace...")
    run_mysql_command(f"ALTER TABLE enb.{TABLE_NAME} DISCARD TABLESPACE;")
    print("✅ Tablespace отключён")
    print()
    
    # Копирование файлов
    print("Копирование .ibd и .frm файлов...")
    print("⚠️  Остановите MySQL 5.7 (Ctrl+C в окне сервера)")
    input("Нажмите Enter когда остановите...")
    
    target_dir = NEW_DATA_DIR / "enb"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(ibd_file, target_dir / f"{TABLE_NAME}.ibd")
    shutil.copy2(frm_file, target_dir / f"{TABLE_NAME}.frm")
    
    print("✅ Файлы скопированы")
    print()
    
    print("Запустите MySQL 5.7 снова и нажмите Enter...")
    input()
    
    # Импорт tablespace
    print("Импорт tablespace...")
    time.sleep(3)  # Даём время серверу запуститься
    
    success, stdout, stderr = run_mysql_command(f"ALTER TABLE enb.{TABLE_NAME} IMPORT TABLESPACE;")
    
    if not success:
        print("❌ Ошибка импорта tablespace")
        print(f"Ошибка: {stderr}")
        return
    
    print("✅ Tablespace импортирован!")
    print()
    
    # Проверка данных
    print("Проверка данных...")
    success, stdout, stderr = run_mysql_command(f"SELECT COUNT(*) as total FROM enb.{TABLE_NAME};")
    
    if success:
        print("✅ Данные доступны!")
        print(stdout)
    else:
        print("⚠️  Не удалось получить данные")
        print(stderr)
    
    print("\n" + "="*80)
    print("✅ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО!")
    print("="*80)
    print("\nТеперь можно создать дамп:")
    print(f"  cd {MYSQL57_BIN}")
    print(f"  .\\mysqldump.exe -u root --protocol=TCP enb {TABLE_NAME} > {TABLE_NAME}_dump.sql")


if __name__ == "__main__":
    main()
