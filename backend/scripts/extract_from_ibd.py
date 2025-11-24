"""
Извлечение данных из .ibd файлов MySQL напрямую
Использует утилиту innodb_space или прямое чтение
"""
import struct
import os
from pathlib import Path

IBD_DIR = Path(r"C:\python\sites_mysql\enb")

def read_ibd_header(ibd_file):
    """Читает заголовок .ibd файла"""
    try:
        with open(ibd_file, 'rb') as f:
            # Читаем первые 16KB (стандартный размер страницы InnoDB)
            header = f.read(16384)
            
            # Проверяем FIL_PAGE_TYPE (offset 24-25)
            page_type = struct.unpack('>H', header[24:26])[0]
            
            # Проверяем Space ID (offset 34-37)
            space_id = struct.unpack('>I', header[34:38])[0]
            
            # Проверяем LSN (offset 16-23)
            lsn = struct.unpack('>Q', header[16:24])[0]
            
            return {
                'page_type': page_type,
                'space_id': space_id,
                'lsn': lsn,
                'size': os.path.getsize(ibd_file)
            }
    except Exception as e:
        return {'error': str(e)}

def analyze_tables():
    """Анализ всех .ibd файлов"""
    print("="*80)
    print("📊 АНАЛИЗ .IBD ФАЙЛОВ")
    print("="*80)
    
    tables = ['user', 'companies', 'advert', 'categories', 'file', 'review', 'messages']
    
    for table in tables:
        ibd_file = IBD_DIR / f"{table}.ibd"
        frm_file = IBD_DIR / f"{table}.frm"
        
        if not ibd_file.exists():
            print(f"\n❌ {table}: .ibd файл не найден")
            continue
        
        info = read_ibd_header(ibd_file)
        
        print(f"\n📄 {table}:")
        print(f"   .ibd размер: {info.get('size', 0):,} bytes")
        print(f"   .frm существует: {'✅' if frm_file.exists() else '❌'}")
        
        if 'error' in info:
            print(f"   ❌ Ошибка чтения: {info['error']}")
        else:
            print(f"   Page Type: {info['page_type']}")
            print(f"   Space ID: {info['space_id']}")
            print(f"   LSN: {info['lsn']}")

def suggest_solutions():
    """Предложить решения"""
    print("\n" + "="*80)
    print("💡 ВОЗМОЖНЫЕ РЕШЕНИЯ")
    print("="*80)
    
    print("\n1. Использовать MySQL Utilities для извлечения данных:")
    print("   - Скачать: https://dev.mysql.com/downloads/utilities/")
    print("   - Утилита: mysqlfrm для чтения .frm файлов")
    
    print("\n2. Использовать старый сервер где эти файлы работали:")
    print("   - Найти оригинальный сервер с этой базой")
    print("   - Сделать mysqldump оттуда")
    
    print("\n3. Попробовать разные версии MySQL:")
    print("   - MySQL 5.5.x")
    print("   - MySQL 5.6.x")
    print("   - MariaDB 10.1.x")
    
    print("\n4. Использовать специализированные инструменты:")
    print("   - Percona Data Recovery Tool")
    print("   - innodb_ruby")
    print("   - TwinDB Data Recovery Toolkit")
    
    print("\n5. Восстановить из резервной копии:")
    print("   - Есть ли дамп базы данных?")
    print("   - Есть ли доступ к старому серверу?")

if __name__ == "__main__":
    analyze_tables()
    suggest_solutions()
    
    print("\n" + "="*80)
    print("❓ Вопросы:")
    print("="*80)
    print("1. С какой версии MySQL эти файлы?")
    print("2. Есть ли доступ к старому серверу?")
    print("3. Есть ли SQL дамп базы данных?")
    print("4. Когда последний раз эти файлы работали?")
    print("="*80)
