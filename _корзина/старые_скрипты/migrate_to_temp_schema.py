"""
Миграция данных из SQL файлов в схему temp PostgreSQL
"""
import os
import re
import asyncio
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Настройки подключения к PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"

# Путь к корневой директории проекта
BASE_DIR = Path(__file__).parent.parent.parent

# SQL файлы для миграции
SQL_FILES = [
    'seller_inserts.sql',
    'categories_inserts.sql',
    'companies_inserts.sql',
    'sub_categories_inserts.sql',
    'user_inserts.sql',
    'review_inserts.sql',
    'file_inserts.sql',
    'advert_inserts.sql',
]


def parse_create_table(sql_content: str) -> tuple[str, str]:
    """
    Извлекает имя таблицы и SQL для создания таблицы
    """
    # Ищем CREATE TABLE
    create_match = re.search(
        r'CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\)\s*ENGINE',
        sql_content,
        re.DOTALL | re.IGNORECASE
    )
    
    if not create_match:
        raise ValueError("Не найден CREATE TABLE в SQL")
    
    table_name = create_match.group(1)
    columns_def = create_match.group(2)
    
    # Конвертируем MySQL типы в PostgreSQL
    columns_def = convert_mysql_to_postgres(columns_def)
    
    return table_name, columns_def


def convert_mysql_to_postgres(columns_def: str) -> str:
    """
    Конвертирует типы данных MySQL в PostgreSQL
    """
    # INT PRIMARY KEY AUTO_INCREMENT -> SERIAL PRIMARY KEY
    columns_def = re.sub(
        r'(\w+)\s+INT\s+PRIMARY KEY\s+AUTO_INCREMENT',
        r'\1 SERIAL PRIMARY KEY',
        columns_def,
        flags=re.IGNORECASE
    )
    
    # INT -> INTEGER
    columns_def = re.sub(r'\bINT\b', 'INTEGER', columns_def, flags=re.IGNORECASE)
    
    # VARCHAR(255) -> VARCHAR(255) (оставляем как есть)
    
    # TEXT -> TEXT (оставляем как есть)
    
    # DEFAULT NULL -> DEFAULT NULL (оставляем как есть)
    
    # Убираем CHARSET и COLLATE
    columns_def = re.sub(r'CHARACTER SET \w+', '', columns_def, flags=re.IGNORECASE)
    columns_def = re.sub(r'COLLATE \w+', '', columns_def, flags=re.IGNORECASE)
    
    return columns_def


def extract_insert_statements(sql_content: str) -> list[str]:
    """
    Извлекает все INSERT INTO statements
    """
    # Ищем все INSERT INTO
    inserts = re.findall(
        r'INSERT INTO \w+.*?;',
        sql_content,
        re.DOTALL | re.IGNORECASE
    )
    
    return inserts


def convert_insert_to_postgres(insert_sql: str, table_name: str, schema: str = 'temp') -> str:
    """
    Конвертирует INSERT statement для PostgreSQL
    """
    # Заменяем имя таблицы на temp.table_name
    insert_sql = re.sub(
        rf'INSERT INTO {table_name}',
        f'INSERT INTO {schema}.{table_name}',
        insert_sql,
        flags=re.IGNORECASE
    )
    
    # UNIX_TIMESTAMP() -> EXTRACT(EPOCH FROM NOW())::INTEGER
    insert_sql = re.sub(
        r'UNIX_TIMESTAMP\(\)',
        "EXTRACT(EPOCH FROM NOW())::INTEGER",
        insert_sql,
        flags=re.IGNORECASE
    )
    
    return insert_sql


async def create_temp_schema(session: AsyncSession):
    """
    Создает схему temp если её нет
    """
    print("📁 Создаём схему temp...")
    await session.execute(text("CREATE SCHEMA IF NOT EXISTS temp"))
    await session.commit()
    print("✅ Схема temp создана")


async def create_table_in_temp(session: AsyncSession, table_name: str, columns_def: str):
    """
    Создает таблицу в схеме temp
    """
    print(f"📋 Создаём таблицу temp.{table_name}...")
    
    # Удаляем таблицу если существует
    await session.execute(text(f"DROP TABLE IF EXISTS temp.{table_name} CASCADE"))
    
    # Создаём таблицу
    create_sql = f"""
    CREATE TABLE temp.{table_name} (
        {columns_def}
    )
    """
    
    await session.execute(text(create_sql))
    await session.commit()
    print(f"✅ Таблица temp.{table_name} создана")


async def insert_data(session: AsyncSession, insert_statements: list[str], table_name: str):
    """
    Вставляет данные в таблицу
    """
    print(f"📥 Загружаем данные в temp.{table_name}...")
    
    total = len(insert_statements)
    batch_size = 100  # Уменьшаем размер батча для лучшей обработки ошибок
    errors = 0
    success = 0
    
    for i in range(0, total, batch_size):
        batch = insert_statements[i:i + batch_size]
        
        for insert_sql in batch:
            try:
                # Конвертируем INSERT для PostgreSQL
                pg_insert = convert_insert_to_postgres(insert_sql, table_name)
                await session.execute(text(pg_insert))
                await session.commit()  # Коммитим каждую запись отдельно
                success += 1
            except Exception as e:
                errors += 1
                await session.rollback()  # Откатываем транзакцию при ошибке
                if errors <= 5:  # Показываем только первые 5 ошибок
                    error_msg = str(e).replace('\n', ' ')[:200]
                    print(f"⚠️ Ошибка #{errors}: {error_msg}")
                continue
        
        # Показываем прогресс
        if (i + batch_size) % 1000 == 0 or i + batch_size >= total:
            print(f"  ✓ Обработано: {min(i + batch_size, total)}/{total} | Успешно: {success} | Ошибок: {errors}")
    
    # Получаем количество записей
    result = await session.execute(text(f"SELECT COUNT(*) FROM temp.{table_name}"))
    count = result.scalar()
    
    if errors > 0:
        print(f"⚠️ Пропущено {errors} записей из-за ошибок")
    print(f"✅ Загружено {count} записей в temp.{table_name}")


async def migrate_file(session: AsyncSession, sql_file: str):
    """
    Мигрирует один SQL файл
    """
    file_path = BASE_DIR / sql_file
    
    if not file_path.exists():
        print(f"⚠️ Файл не найден: {sql_file}")
        return
    
    print(f"\n{'='*60}")
    print(f"🔄 Обрабатываем: {sql_file}")
    print(f"{'='*60}")
    
    # Читаем файл
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    try:
        # Парсим CREATE TABLE
        table_name, columns_def = parse_create_table(sql_content)
        
        # Создаём таблицу
        await create_table_in_temp(session, table_name, columns_def)
        
        # Извлекаем INSERT statements
        insert_statements = extract_insert_statements(sql_content)
        
        if insert_statements:
            # Вставляем данные
            await insert_data(session, insert_statements, table_name)
        else:
            print(f"⚠️ Нет данных для вставки в {table_name}")
    
    except Exception as e:
        print(f"❌ Ошибка при обработке {sql_file}: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """
    Главная функция миграции
    """
    print("🚀 Начинаем миграцию данных в схему temp...")
    print(f"📊 База данных: {DATABASE_URL}")
    print(f"📁 Файлов для миграции: {len(SQL_FILES)}")
    
    # Создаём engine и session
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Создаём схему temp
        await create_temp_schema(session)
        
        # Мигрируем каждый файл
        for sql_file in SQL_FILES:
            await migrate_file(session, sql_file)
    
    await engine.dispose()
    
    print("\n" + "="*60)
    print("🎉 Миграция завершена!")
    print("="*60)
    print("\n📊 Проверка данных:")
    print("SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'temp';")
    print("\nПример запроса:")
    print("SELECT * FROM temp.categories LIMIT 10;")


if __name__ == "__main__":
    asyncio.run(main())
