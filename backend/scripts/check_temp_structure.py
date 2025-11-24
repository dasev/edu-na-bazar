"""
Проверка структуры таблиц в схеме temp
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def check_structure():
    """Проверяет структуру таблиц"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("📊 СТРУКТУРА ТАБЛИЦ В СХЕМЕ TEMP")
        print("="*80)
        print()
        
        tables = ['seller', 'categories', 'companies', 'sub_categories', 
                  'user', 'review', 'file', 'advert']
        
        for table in tables:
            try:
                print(f"\n{'='*80}")
                print(f"📋 {table.upper()}")
                print(f"{'='*80}")
                
                # Получаем структуру
                result = await session.execute(text(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'temp' AND table_name = '{table}'
                    ORDER BY ordinal_position
                """))
                
                columns = []
                for row in result:
                    columns.append(row[0])
                    nullable = 'NULL' if row[2] == 'YES' else 'NOT NULL'
                    print(f"   {row[0]:25} {row[1]:20} {nullable}")
                
                # Получаем количество записей
                result = await session.execute(text(f"SELECT COUNT(*) FROM temp.{table}"))
                count = result.scalar()
                print(f"\n   📊 Всего записей: {count}")
                
                # Показываем первую запись
                if count > 0:
                    cols_str = ', '.join(columns[:10])  # Первые 10 колонок
                    result = await session.execute(text(f"SELECT {cols_str} FROM temp.{table} LIMIT 1"))
                    row = result.first()
                    if row:
                        print(f"\n   📄 Пример данных (первая запись):")
                        for i, col in enumerate(columns[:10]):
                            value = row[i] if i < len(row) else 'N/A'
                            if isinstance(value, str) and len(value) > 50:
                                value = value[:50] + '...'
                            print(f"      {col}: {value}")
                
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        print(f"\n{'='*80}")
        print("✅ ПРОВЕРКА ЗАВЕРШЕНА")
        print(f"{'='*80}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_structure())
