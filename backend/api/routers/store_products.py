"""
Store Products Router - управление товарами магазина
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from services.jwt_service import JWTService

router = APIRouter(prefix="/api/my-stores", tags=["store-products"])


async def get_current_user(
    authorization: str = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из токена"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная схема авторизации")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена")
    
    payload = JWTService.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    
    # Конвертируем строку в int
    try:
        user_id = int(user_id_str)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат ID пользователя"
        )
    
    # Получаем пользователя из БД
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user


@router.get("/{store_id}/products", response_model=ProductListResponse)
async def get_store_products(
    store_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить все товары магазина"""
    # Проверяем что магазин принадлежит пользователю
    result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден или не принадлежит вам"
        )
    
    # Получаем товары магазина
    query = select(Product).where(Product.store_owner_id == store_id)
    
    # Подсчет общего количества
    from sqlalchemy import func
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Получаем товары с пагинацией
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    
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


@router.post("/{store_id}/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_store_product(
    store_id: int,
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создать товар для магазина"""
    # Проверяем что магазин принадлежит пользователю
    result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден или не принадлежит вам"
        )
    
    # Создаем товар
    product_dict = product_data.model_dump()
    product_dict['store_owner_id'] = store_id
    product = Product(**product_dict)
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return product


@router.put("/{store_id}/products/{product_id}", response_model=ProductResponse)
async def update_store_product(
    store_id: int,
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновить товар магазина"""
    # Проверяем что магазин принадлежит пользователю
    result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден или не принадлежит вам"
        )
    
    # Получаем товар
    result = await db.execute(
        select(Product).where(
            and_(
                Product.id == product_id,
                Product.store_owner_id == store_id
            )
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    # Обновляем товар
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    
    return product


@router.delete("/{store_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store_product(
    store_id: int,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить товар магазина"""
    # Проверяем что магазин принадлежит пользователю
    result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден или не принадлежит вам"
        )
    
    # Получаем товар
    result = await db.execute(
        select(Product).where(
            and_(
                Product.id == product_id,
                Product.store_owner_id == store_id
            )
        )
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    # Удаляем товар
    await db.delete(product)
    await db.commit()
