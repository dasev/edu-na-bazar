import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/edu_na_bazar')
    rows = await conn.fetch("SELECT name, rating, reviews_count FROM market.products WHERE name LIKE '%луговое%' OR name LIKE '%Сено%' LIMIT 5")
    
    print("\n📊 Проверка рейтингов в БД:\n")
    for row in rows:
        print(f"  {row['name']}: ⭐ {row['rating']:.1f} ({row['reviews_count']} отзывов)")
    
    await conn.close()

asyncio.run(check())
