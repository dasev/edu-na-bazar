"""
Moderation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List

from database import get_db
from models.user import User
from models.product import Product
from models.moderation import ModerationLog
from api.dependencies import get_current_user
from schemas.product import ProductResponse, ProductListResponse

router = APIRouter(prefix="/api/moderation", tags=["moderation"])


@router.get("/products", response_model=ProductListResponse)
async def get_moderation_products(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить товары на модерации (только для модераторов)"""
    if not current_user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуются права модератора."
        )
    
    print(f"📋 Получение товаров на модерации, модератор={current_user.id}")
    
    # Получаем товары на модерации
    query = select(Product).where(Product.status == "moderation")
    
    # Подсчет общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Получаем товары с пагинацией
    query = query.offset(skip).limit(limit).order_by(Product.created_at.desc())
    result = await db.execute(query)
    products = result.scalars().all()
    
    print(f"  Найдено товаров на модерации: {total}")
    
    return ProductListResponse(
        data=products,
        meta={
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1,
        }
    )


@router.patch("/products/{product_id}/approve", status_code=status.HTTP_200_OK)
async def approve_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Одобрить товар (модератор)"""
    if not current_user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуются права модератора."
        )
    
    print(f"✅ Одобрение товара {product_id}, модератор={current_user.id}")
    
    # Получаем товар
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    if product.status != "moderation":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Товар не на модерации (статус: {product.status})"
        )
    
    # Одобряем товар
    product.status = "active"
    
    # Сохраняем лог модерации
    log = ModerationLog(
        product_id=product_id,
        moderator_id=current_user.id,
        action="approved"
    )
    db.add(log)
    
    await db.commit()
    
    print(f"✅ Товар {product_id} одобрен и опубликован")
    
    return {"message": "Товар одобрен", "product_id": product_id}


@router.patch("/products/{product_id}/reject", status_code=status.HTTP_200_OK)
async def reject_product(
    product_id: int,
    reason: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Отклонить товар (модератор)"""
    if not current_user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуются права модератора."
        )
    
    print(f"❌ Отклонение товара {product_id}, модератор={current_user.id}, причина={reason}")
    
    # Получаем товар
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    if product.status != "moderation":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Товар не на модерации (статус: {product.status})"
        )
    
    # Отклоняем товар - возвращаем в черновики
    product.status = "rejected"
    
    # Сохраняем лог модерации с причиной
    log = ModerationLog(
        product_id=product_id,
        moderator_id=current_user.id,
        action="rejected",
        reason=reason
    )
    db.add(log)
    
    await db.commit()
    
    print(f"❌ Товар {product_id} отклонен")
    
    return {"message": "Товар отклонен", "product_id": product_id, "reason": reason}
