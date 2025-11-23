"""
Создание всех таблиц в БД через SQLAlchemy
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base
from config import settings

# Импортируем все модели чтобы они зарегистрировались в Base.metadata
from models.user import User, SMSCode
from models.category import Category
from models.product import Product
from models.store import Store
from models.order import Order, OrderItem
from models.cart import CartItem


async def create_tables():
    """Создать все таблицы"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    print("🚀 Создаем все таблицы в БД...\n")
    
    async with engine.begin() as conn:
        # Создаем расширение PostGIS
        await conn.run_sync(lambda sync_conn: sync_conn.execute("CREATE EXTENSION IF NOT EXISTS postgis"))
        print("✅ PostGIS extension создан\n")
        
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Все таблицы созданы!\n")
    
    await engine.dispose()
    print("🎉 Готово!")


if __name__ == "__main__":
    asyncio.run(create_tables())
