"""
Экспорт данных из старой базы MySQL используя прямое чтение файлов
или создание дампа
"""
import subprocess
import os

MARIADB_BIN = r"C:\Program Files\MariaDB 12.1\bin"
OUTPUT_FILE = r"C:\python\edu-na-bazar\enb_export.sql"

def export_with_mysqldump():
    """Экспорт через mysqldump"""
    print("="*80)
    print("📤 ЭКСПОРТ ДАННЫХ ЧЕРЕЗ MYSQLDUMP")
    print("="*80)
    
    tables = ['user', 'companies', 'advert', 'categories', 'file', 'review', 'messages', 'city', 'region']
    
    cmd = [
        os.path.join(MARIADB_BIN, "mysqldump.exe"),
        "-u", "root",
        "-proot",
        "--skip-lock-tables",
        "--no-create-info",  # Только данные, без CREATE TABLE
        "--complete-insert",  # Полные INSERT с именами колонок
        "--skip-extended-insert",  # Каждая строка отдельно
        "enb"
    ] + tables
    
    print(f"Команда: {' '.join(cmd)}")
    print(f"Выходной файл: {OUTPUT_FILE}")
    print()
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode == 0:
            size = os.path.getsize(OUTPUT_FILE)
            print(f"✅ Экспорт успешен! Размер файла: {size:,} bytes")
            print(f"📄 Файл: {OUTPUT_FILE}")
            return True
        else:
            print(f"❌ Ошибка: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def show_table_info():
    """Показать информацию о таблицах"""
    print("\n" + "="*80)
    print("📊 ИНФОРМАЦИЯ О ТАБЛИЦАХ")
    print("="*80)
    
    tables = ['user', 'companies', 'advert', 'categories']
    
    for table in tables:
        cmd = [
            os.path.join(MARIADB_BIN, "mysql.exe"),
            "-u", "root",
            "-proot",
            "enb",
            "-e", f"SELECT COUNT(*) as count FROM {table};"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    count = lines[1]
                    print(f"  {table:20} {count:>10} записей")
            else:
                print(f"  {table:20} ❌ Ошибка")
        except Exception as e:
            print(f"  {table:20} ❌ {e}")

if __name__ == "__main__":
    show_table_info()
    print()
    export_with_mysqldump()
