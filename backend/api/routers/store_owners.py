"""
Store Owners Public Router - публичный доступ к магазинам
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{store_owner_id}", response_model=StoreOwnerResponse)
async def get_store_owner(store_owner_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о продавце по ID (публичный endpoint)
    """
    query = select(StoreOwner).where(StoreOwner.id == store_owner_id)
    result = await db.execute(query)
    store_owner = result.scalar_one_or_none()
    
    if not store_owner:
        raise HTTPException(status_code=404, detail="Продавец не найден")
    
    return store_owner
