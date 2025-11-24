"""
Перезагрузка только таблицы temp.file со связями
"""
import asyncio
import re
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"
BASE_DIR = Path(__file__).parent.parent.parent
SQL_FILE = BASE_DIR / "file_inserts.sql"


def convert_mysql_to_postgres(sql: str) -> str:
    """Конвертирует MySQL синтаксис в PostgreSQL"""
    # AUTO_INCREMENT → SERIAL
    sql = re.sub(r'INT\s+PRIMARY\s+KEY\s+AUTO_INCREMENT', 'SERIAL PRIMARY KEY', sql, flags=re.IGNORECASE)
    
    # ENGINE=InnoDB → убираем
    sql = re.sub(r'ENGINE\s*=\s*\w+', '', sql, flags=re.IGNORECASE)
    
    # DEFAULT CHARSET → убираем
    sql = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', sql, flags=re.IGNORECASE)
    
    # UNIX_TIMESTAMP() → EXTRACT(EPOCH FROM NOW())::INTEGER
    sql = re.sub(r'UNIX_TIMESTAMP\(\)', 'EXTRACT(EPOCH FROM NOW())::INTEGER', sql, flags=re.IGNORECASE)
    
    return sql


async def reload_file_table():
    """Перезагружает таблицу temp.file"""
    
    print("="*80)
    print("🔄 ПЕРЕЗАГРУЗКА ТАБЛИЦЫ temp.file СО СВЯЗЯМИ")
    print("="*80)
    print()
    
    if not SQL_FILE.exists():
        print(f"❌ Файл не найден: {SQL_FILE}")
        return
    
    print(f"📁 Файл: {SQL_FILE}")
    print(f"📊 Размер: {SQL_FILE.stat().st_size / 1024 / 1024:.1f} MB")
    print()
    
    # Читаем SQL файл
    print("📖 Читаем SQL файл...")
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Извлекаем CREATE TABLE (только до первой точки с запятой)
    create_match = re.search(r'(CREATE TABLE.*?file\s*\(.*?\);)', content, re.DOTALL | re.IGNORECASE)
    if not create_match:
        print("❌ CREATE TABLE не найден")
        return
    
    create_table = create_match.group(1)
    # Убираем всё после закрывающей скобки и точки с запятой
    create_table = re.sub(r'\);.*', ');', create_table, flags=re.DOTALL)
    
    # Извлекаем INSERT запросы
    insert_pattern = re.compile(r'INSERT INTO file.*?;', re.DOTALL | re.IGNORECASE)
    inserts = insert_pattern.findall(content)
    
    print(f"✅ Найдено INSERT запросов: {len(inserts)}")
    print()
    
    # Подключаемся к БД
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Удаляем старую таблицу
        print("🗑️ Удаляем старую таблицу temp.file...")
        await session.execute(text("DROP TABLE IF EXISTS temp.file CASCADE"))
        await session.commit()
        print("✅ Таблица удалена")
        print()
        
        # Создаём новую таблицу
        print("📋 Создаём таблицу temp.file...")
        
        # Конвертируем CREATE TABLE для PostgreSQL
        pg_create = convert_mysql_to_postgres(create_table)
        # Заменяем CREATE TABLE IF NOT EXISTS file на CREATE TABLE temp.file
        pg_create = re.sub(r'CREATE TABLE\s+IF\s+NOT\s+EXISTS\s+file', 'CREATE TABLE temp.file', pg_create, flags=re.IGNORECASE)
        pg_create = re.sub(r'CREATE TABLE\s+file', 'CREATE TABLE temp.file', pg_create, flags=re.IGNORECASE)
        
        await session.execute(text(pg_create))
        await session.commit()
        print("✅ Таблица создана")
        print()
        
        # Загружаем данные
        print(f"📥 Загружаем данные ({len(inserts)} записей)...")
        
        batch_size = 100
        success = 0
        errors = 0
        
        for i in range(0, len(inserts), batch_size):
            batch = inserts[i:i + batch_size]
            
            for insert_sql in batch:
                try:
                    # Конвертируем INSERT для PostgreSQL
                    pg_insert = convert_mysql_to_postgres(insert_sql)
                    pg_insert = re.sub(r'INSERT INTO\s+file', 'INSERT INTO temp.file', pg_insert, flags=re.IGNORECASE)
                    
                    await session.execute(text(pg_insert))
                    await session.commit()
                    success += 1
                except Exception as e:
                    errors += 1
                    await session.rollback()
                    if errors <= 5:
                        error_msg = str(e).replace('\n', ' ')[:150]
                        print(f"   ⚠️ Ошибка #{errors}: {error_msg}")
                    continue
            
            # Показываем прогресс
            if (i + batch_size) % 1000 == 0 or i + batch_size >= len(inserts):
                print(f"   ✓ Обработано: {min(i + batch_size, len(inserts))}/{len(inserts)} | Успешно: {success} | Ошибок: {errors}")
        
        print()
        
        # Проверяем результат
        print("📊 Проверка результата:")
        
        result = await session.execute(text("SELECT COUNT(*) FROM temp.file"))
        total = result.scalar()
        print(f"   Всего записей: {total}")
        
        result = await session.execute(text("""
            SELECT 
                COUNT(CASE WHEN advert_id IS NOT NULL THEN 1 END) as with_advert,
                COUNT(CASE WHEN company_id IS NOT NULL THEN 1 END) as with_company
            FROM temp.file
            WHERE type = 'image'
        """))
        row = result.first()
        print(f"   С advert_id: {row[0]}")
        print(f"   С company_id: {row[1]}")
        
        # Примеры
        result = await session.execute(text("""
            SELECT id, filename, advert_id, company_id
            FROM temp.file
            WHERE type = 'image' AND advert_id IS NOT NULL
            LIMIT 5
        """))
        
        print(f"\n   📸 Примеры с advert_id:")
        for r in result:
            print(f"      ID: {r[0]}, File: {r[1][:40]}, Advert: {r[2]}, Company: {r[3]}")
    
    await engine.dispose()
    
    print()
    print("="*80)
    print("✅ ПЕРЕЗАГРУЗКА ЗАВЕРШЕНА!")
    print("="*80)
    print()
    print(f"📊 Итого:")
    print(f"   Загружено: {success}")
    print(f"   Ошибок: {errors}")
    print()


if __name__ == "__main__":
    asyncio.run(reload_file_table())
