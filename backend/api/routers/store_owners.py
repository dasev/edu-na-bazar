"""
Store Owners Public Router - публичный доступ к магазинам
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.store_owner import StoreOwner
from schemas.store_owner import StoreOwnerResponse

router = APIRouter(prefix="/api/store-owners", tags=["store-owners"])


@router.get("/all", response_model=List[StoreOwnerResponse])
async def get_all_stores(db: AsyncSession = Depends(get_db)):
    """
    Получить все активные магазины (публичный endpoint)
    """
    query = select(StoreOwner).where(StoreOwner.status == 'approved')
    result = await db.execute(query)
    stores = result.scalars().all()
    return stores
