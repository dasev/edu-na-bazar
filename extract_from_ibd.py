"""
Попытка извлечь данные из .ibd файла напрямую
Используем библиотеку undrop-for-innodb или прямое чтение
"""
import struct
import os

IBD_FILE = r"C:\python\sites_mysql\enb\companies.ibd"

def read_ibd_header(filename):
    """Читаем заголовок InnoDB файла"""
    with open(filename, 'rb') as f:
        # Читаем первую страницу (16KB)
        page = f.read(16384)
        
        # Проверяем magic number
        magic = struct.unpack('>I', page[0:4])[0]
        print(f"Magic number: {hex(magic)}")
        
        # Page type
        page_type = struct.unpack('>H', page[24:26])[0]
        print(f"Page type: {page_type}")
        
        # Space ID
        space_id = struct.unpack('>I', page[34:38])[0]
        print(f"Space ID: {space_id}")
        
        # Размер файла
        file_size = os.path.getsize(filename)
        num_pages = file_size // 16384
        print(f"Файл: {file_size / 1024 / 1024:.1f} MB")
        print(f"Страниц: {num_pages}")
        
        return page

if __name__ == "__main__":
    print("Анализ .ibd файла...")
    print(f"Файл: {IBD_FILE}")
    print()
    
    try:
        header = read_ibd_header(IBD_FILE)
        print("\n✅ Файл читается, но для полного восстановления нужны специальные утилиты")
        print("\nРЕКОМЕНДАЦИЯ:")
        print("Используйте утилиту 'undrop-for-innodb' или 'innodb_space'")
        print("Или найдите оригинальный SQL дамп базы данных")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
