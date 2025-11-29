"""
My Stores Router - управление магазинами пользователя
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from models.order import Order, OrderItem
from models.product import Product
from schemas.store_owner import StoreOwnerCreate, StoreOwnerResponse, StoreOwnerUpdate
from schemas.order import OrderResponse, OrderListResponse, OrderUpdateStatus
from services.jwt_service import JWTService
from services.image_service import ImageService
import os
import uuid

router = APIRouter(prefix="/api/my-stores", tags=["my-stores"])


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
    
    # Извлекаем токен из заголовка "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверная схема авторизации"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена"
        )
    
    # Проверяем токен
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    return user


@router.get("", response_model=List[StoreOwnerResponse])
async def get_my_stores(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список магазинов текущего пользователя
    """
    try:
        from sqlalchemy import func
        from models.product import Product
        
        print(f"📋 Получение магазинов для user_id={current_user.id}")
        
        result = await db.execute(
            select(StoreOwner).where(StoreOwner.owner_id == current_user.id)
        )
        stores = result.scalars().all()
        
        print(f"  Найдено магазинов: {len(stores)}")
        
        # Добавляем количество товаров для каждого магазина
        stores_with_count = []
        for store in stores:
            print(f"  Обработка магазина {store.id}: {store.name}")
            # Подсчитываем активные товары
            active_count_result = await db.execute(
                select(func.count(Product.id)).where(
                    and_(
                        Product.store_owner_id == store.id,
                        Product.status == "active"
                    )
                )
            )
            products_count = active_count_result.scalar() or 0
            print(f"    Активных товаров: {products_count}")
            
            # Создаем словарь с данными магазина
            store_dict = {
                "id": store.id,
                "owner_id": store.owner_id,
                "inn": store.inn,
                "kpp": store.kpp,
                "ogrn": store.ogrn,
                "name": store.name,
                "legal_name": store.legal_name,
                "address": store.address,
                "phone": store.phone,
                "email": store.email,
                "description": store.description,
                "logo": store.logo,
                "banner": store.banner,
                "status": store.status,
                "created_at": store.created_at,
                "updated_at": store.updated_at,
                "products_count": products_count
            }
            stores_with_count.append(store_dict)
        
        print(f"✅ Возвращаем {len(stores_with_count)} магазинов")
        return stores_with_count
    
    except Exception as e:
        import traceback
        print(f"❌ Ошибка в get_my_stores: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения магазинов: {str(e)}"
        )


@router.get("/{store_id}", response_model=StoreOwnerResponse)
async def get_store(
    store_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить магазин по ID
    """
    # Получаем магазин
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
            detail="Магазин не найден"
        )
    
    return store


@router.post("", response_model=StoreOwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreOwnerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новый магазин
    """
    # Проверяем уникальность ИНН
    existing_store = await db.execute(
        select(StoreOwner).where(StoreOwner.inn == store_data.inn)
    )
    if existing_store.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Магазин с ИНН {store_data.inn} уже существует"
        )
    
    # Создаем магазин
    new_store = StoreOwner(
        owner_id=current_user.id,
        inn=store_data.inn,
        kpp=store_data.kpp,
        ogrn=store_data.ogrn,
        name=store_data.name,
        legal_name=store_data.legal_name,
        address=store_data.address,
        phone=store_data.phone,
        email=store_data.email,
        description=store_data.description
    )
    
    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)
    
    return new_store


@router.put("/{store_id}", response_model=StoreOwnerResponse)
async def update_store(
    store_id: int,
    store_data: StoreOwnerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить магазин
    """
    # Получаем магазин
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
            detail="Магазин не найден"
        )
    
    # Обновляем поля
    update_data = store_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(store, field, value)
    
    try:
        await db.commit()
        await db.refresh(store)
        return store
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления магазина: {str(e)}"
        )


@router.delete("/{store_id}")
async def delete_store(
    store_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить магазин
    """
    # TODO: Реализовать когда будет модель Store
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


# Endpoints для товаров перенесены в store_products.py


@router.post("/products/{product_id}/images")
async def upload_product_image(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Загрузить изображение товара
    """
    # TODO: Реализовать когда будет модель StoreProduct
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


# Endpoints для заказов магазина
@router.get("/{store_id}/orders", response_model=OrderListResponse)
async def get_store_orders(
    store_id: int,
    status_filter: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить заказы магазина
    """
    # Проверяем что магазин принадлежит пользователю
    store_result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден"
        )
    
    # Получаем заказы с товарами из этого магазина
    query = (
        select(Order)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Product.store_owner_id == store_id)
        .options(selectinload(Order.items))
        .distinct()
    )
    
    if status_filter:
        query = query.where(Order.status == status_filter)
    
    # Подсчет
    count_query = (
        select(func.count(func.distinct(Order.id)))
        .select_from(Order)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Product.store_owner_id == store_id)
    )
    if status_filter:
        count_query = count_query.where(Order.status == status_filter)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Сортировка и пагинация
    query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # Преобразуем в словари с загрузкой информации о товарах
    orders_data = []
    for order in orders:
        # Загружаем товары для items
        items_with_products = []
        for item in order.items:
            # Получаем товар
            product_result = await db.execute(
                select(Product).where(Product.id == item.product_id)
            )
            product = product_result.scalar_one_or_none()
            
            items_with_products.append({
                "id": item.id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "product_name": product.name if product else f"Товар {item.product_id}",
                "product_image": product.image if product else None,
                "quantity": item.quantity,
                "price": float(item.price),
                "subtotal": item.subtotal,
                "created_at": item.created_at,
            })
        
        orders_data.append({
            "id": order.id,
            "user_id": order.user_id,
            "store_id": order.store_id,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "delivery_address": order.delivery_address,
            "delivery_phone": order.delivery_phone,
            "payment_method": order.payment_method,
            "notes": order.notes,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "items": items_with_products
        })
    
    return OrderListResponse(
        data=orders_data,
        meta={
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1,
        }
    )


@router.put("/{store_id}/orders/{order_id}/status", response_model=OrderResponse)
async def update_store_order_status(
    store_id: int,
    order_id: int,
    status_data: OrderUpdateStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить статус заказа (только для владельца магазина)
    """
    # Проверяем что магазин принадлежит пользователю
    store_result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == current_user.id
            )
        )
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден"
        )
    
    # Получаем заказ
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Обновляем статус
    order.status = status_data.status
    
    await db.commit()
    
    # Загружаем заново
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    updated_order = result.scalar_one()
    
    # Преобразуем в словарь
    order_dict = {
        "id": updated_order.id,
        "user_id": updated_order.user_id,
        "store_id": updated_order.store_id,
        "status": updated_order.status,
        "total_amount": float(updated_order.total_amount),
        "delivery_address": updated_order.delivery_address,
        "delivery_phone": updated_order.delivery_phone,
        "payment_method": updated_order.payment_method,
        "notes": updated_order.notes,
        "created_at": updated_order.created_at,
        "updated_at": updated_order.updated_at,
        "items": [
            {
                "id": item.id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "subtotal": item.subtotal,
                "created_at": item.created_at,
            }
            for item in updated_order.items
        ]
    }
    
    return order_dict


@router.post("/{store_id}/logo")
async def upload_store_logo(
    store_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Загрузить логотип магазина"""
    # Проверяем что магазин принадлежит пользователю
    result = await db.execute(
        select(StoreOwner).where(
            and_(
                StoreOwner.id == store_id,
                StoreOwner.owner_id == user.id
            )
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Магазин не найден"
        )
    
    # Проверяем тип файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть изображением"
        )
    
    # Создаем директорию для логотипов если её нет
    upload_dir = "uploads/stores/logos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Генерируем уникальное имя файла
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Сохраняем файл
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Оптимизируем изображение
    try:
        optimized_path = ImageService.optimize_image(file_path, max_size=(400, 400))
        # Удаляем оригинал
        if os.path.exists(file_path):
            os.remove(file_path)
        file_path = optimized_path
    except Exception as e:
        print(f"Ошибка оптимизации: {e}")
    
    # Обновляем путь к логотипу в БД
    logo_url = f"/{file_path}"
    store.logo = logo_url
    await db.commit()
    
    return {"logo_url": logo_url}
