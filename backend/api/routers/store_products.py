"""
Store Products Router - управление товарами магазина
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from models.product import Product
from models.product_image import ProductImage
from models.moderation import ModerationLog
from schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from services.jwt_service import JWTService

router = APIRouter(prefix="/api/my-stores", tags=["store-products"])


async def get_current_user(
    authorization: Optional[str] = Header(None),
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
    
    payload = JWTService.verify_token(token)
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
    status: str = "active",  # active, draft, all
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить товары магазина (по умолчанию только активные)"""
    print(f"🔍 GET /{store_id}/products вызван! user_id={current_user.id}, status={status}")
    
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
    
    # Получаем товары магазина с фильтром по статусу
    query = select(Product).where(Product.store_owner_id == store_id)
    
    if status == "active":
        query = query.where(Product.status == "active")
    elif status == "draft":
        query = query.where(Product.status == "draft")
    elif status == "moderation":
        query = query.where(Product.status == "moderation")
    elif status == "rejected":
        query = query.where(Product.status == "rejected")
    # если status == "all", не добавляем фильтр
    
    # Подсчет общего количества
    from sqlalchemy import func
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    print(f"📦 Получение товаров магазина {store_id}")
    print(f"  Всего товаров: {total}")
    print(f"  skip={skip}, limit={limit}")
    
    # Получаем товары с пагинацией
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    
    print(f"  Получено товаров: {len(products)}")
    for p in products:
        print(f"    - {p.id}: {p.name} (store_owner_id={p.store_owner_id})")
        print(f"      images: {len(p.images) if p.images else 0} шт")
        if p.images:
            for img in p.images:
                print(f"        * {img.image_url}")
    
    try:
        response = ProductListResponse(
            data=products,
            meta={
                "total": total,
                "skip": skip,
                "limit": limit,
                "page": (skip // limit) + 1 if limit > 0 else 1,
                "pages": (total + limit - 1) // limit if limit > 0 else 1,
            }
        )
        print(f"✅ Response created successfully")
        return response
    except Exception as e:
        import traceback
        print(f"❌ Ошибка создания ответа: {e}")
        traceback.print_exc()
        raise


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
    
    # Обрабатываем массив изображений отдельно
    images_urls = product_dict.pop('images', None)
    
    product_dict['store_owner_id'] = store_id
    product = Product(**product_dict)
    
    db.add(product)
    await db.flush()  # Получаем ID товара без коммита
    
    # Если есть массив изображений, добавляем их в product_images
    if images_urls and isinstance(images_urls, list):
        for idx, img_url in enumerate(images_urls):
            if img_url:  # Пропускаем пустые URL
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    is_main=(idx == 0),  # Первое изображение - основное
                    sort_order=idx
                )
                db.add(product_image)
    
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
    
    # Обрабатываем массив изображений отдельно
    images_urls = update_data.pop('images', None)
    
    # Обновляем остальные поля
    for field, value in update_data.items():
        setattr(product, field, value)
    
    # Если есть массив изображений, обновляем таблицу product_images
    if images_urls is not None and isinstance(images_urls, list):
        # Удаляем старые изображения
        await db.execute(
            delete(ProductImage).where(ProductImage.product_id == product_id)
        )
        
        # Добавляем новые изображения
        for idx, img_url in enumerate(images_urls):
            if img_url:  # Пропускаем пустые URL
                product_image = ProductImage(
                    product_id=product_id,
                    image_url=img_url,
                    is_main=(idx == 0),  # Первое изображение - основное
                    sort_order=idx
                )
                db.add(product_image)
    
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
    try:
        print(f"🗑️ DELETE /{store_id}/products/{product_id} вызван! user_id={current_user.id}")
        
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
        
        print(f"  Магазин найден: {store.name}")
        
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
        
        print(f"  Товар найден: {product.name}")
        
        # Перемещаем товар в корзину (draft) вместо удаления
        product.status = "draft"
        await db.commit()
        
        print(f"✅ Товар {product_id} перемещен в корзину")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Ошибка удаления товара: {e}")
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка удаления товара: {str(e)}"
        )


@router.patch("/{store_id}/products/{product_id}/publish", status_code=status.HTTP_200_OK)
async def publish_product(
    store_id: int,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Опубликовать товар из корзины (draft -> active)"""
    try:
        print(f"📤 PUBLISH /{store_id}/products/{product_id} вызван! user_id={current_user.id}")
        
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
        
        print(f"  Товар найден: {product.name}, текущий статус: {product.status}")
        
        # Отправляем товар на модерацию
        product.status = "moderation"
        await db.commit()
        
        print(f"✅ Товар {product_id} отправлен на модерацию")
        
        return {"message": "Товар опубликован", "product_id": product_id}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Ошибка публикации товара: {e}")
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка публикации товара: {str(e)}"
        )


@router.get("/{store_id}/moderation-notifications")
async def get_moderation_notifications(
    store_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить уведомления о модерации товаров магазина"""
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
    
    # Получаем последние логи модерации для товаров этого магазина
    result = await db.execute(
        select(ModerationLog, Product).join(
            Product, ModerationLog.product_id == Product.id
        ).where(
            Product.store_owner_id == store_id
        ).order_by(ModerationLog.created_at.desc()).limit(10)
    )
    logs = result.all()
    
    notifications = []
    for log, product in logs:
        notifications.append({
            "id": log.id,
            "product_id": product.id,
            "product_name": product.name,
            "action": log.action,
            "reason": log.reason,
            "created_at": log.created_at.isoformat()
        })
    
    return {"notifications": notifications}
