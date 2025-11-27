"""
My Stores Router - управление магазинами пользователя
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from schemas.store_owner import StoreOwnerCreate, StoreOwnerResponse, StoreOwnerUpdate
from services.jwt_service import JWTService

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


@router.get("/{store_id}")
async def get_store(
    store_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить магазин по ID
    """
    # TODO: Реализовать когда будет модель Store
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Магазин не найден"
    )


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


@router.put("/{store_id}")
async def update_store(
    store_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить магазин
    """
    # TODO: Реализовать когда будет модель Store
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
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
