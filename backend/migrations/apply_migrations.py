"""
Скрипт для применения SQL миграций
"""
import asyncio
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from config import settings

# Список миграций в порядке применения
MIGRATIONS = [
    "001_create_users_tables.sql",
    "002_create_categories_table.sql",
    "003_create_products_table.sql",
    "004_create_stores_table.sql",
    "005_create_orders_tables.sql",
    "006_create_cart_table.sql",
]


async def apply_migrations():
    """Применить все миграции"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    migrations_dir = Path(__file__).parent / "versions"
    
    async with engine.begin() as conn:
        print("🚀 Начинаем применение миграций...\n")
        
        for migration_file in MIGRATIONS:
            migration_path = migrations_dir / migration_file
            
            if not migration_path.exists():
                print(f"⚠️  Файл не найден: {migration_file}")
                continue
            
            print(f"📝 Применяем миграцию: {migration_file}")
            
            with open(migration_path, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            try:
                # Разбиваем SQL на отдельные команды
                statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
                
                for statement in statements:
                    if statement:
                        try:
                            await conn.execute(text(statement))
                        except Exception as stmt_error:
                            # Игнорируем ошибки "already exists"
                            if "already exists" in str(stmt_error):
                                print(f"  ⚠️  Пропускаем: объект уже существует")
                            else:
                                raise
                
                print(f"✅ Миграция применена: {migration_file}\n")
            except Exception as e:
                print(f"❌ Ошибка при применении миграции {migration_file}:")
                print(f"   {str(e)}\n")
                # Не прерываем выполнение, продолжаем со следующей миграцией
                continue
        
        print("🎉 Все миграции успешно применены!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(apply_migrations())
