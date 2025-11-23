"""
Тест подключения к БД
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from config import settings
from models.product import Product

async def test_connection():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Простой запрос
        result = await session.execute(text("SELECT COUNT(*) FROM products"))
        count = result.scalar()
        print(f"✅ Товаров в БД: {count}")
        
        # Запрос через ORM
        result = await session.execute(select(Product).limit(5))
        products = result.scalars().all()
        print(f"✅ Загружено товаров через ORM: {len(products)}")
        
        for product in products:
            print(f"  - {product.name}: {product.price}₽")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
