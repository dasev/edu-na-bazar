"""
My Stores Router - управление магазинами пользователя
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user import User
from services.jwt_service import JWTService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/my-stores", tags=["my-stores"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из токена"""
    token = credentials.credentials
    
    # Проверяем токен
    payload = JWTService.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
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


@router.get("")
async def get_my_stores(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список магазинов текущего пользователя
    
    Пока возвращаем пустой список, так как модель Store еще не создана
    """
    # TODO: Когда будет создана модель Store, вернуть реальные данные
    # result = await db.execute(
    #     select(Store).where(Store.owner_id == current_user.id)
    # )
    # stores = result.scalars().all()
    # return stores
    
    # Временно возвращаем пустой список
    return []


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


@router.post("")
async def create_store(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новый магазин
    """
    # TODO: Реализовать когда будет модель Store
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


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


@router.get("/{store_id}/products")
async def get_store_products(
    store_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить товары магазина
    """
    # TODO: Реализовать когда будет модель StoreProduct
    return []


@router.post("/products")
async def create_product(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать товар в магазине
    """
    # TODO: Реализовать когда будет модель StoreProduct
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


@router.put("/products/{product_id}")
async def update_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить товар
    """
    # TODO: Реализовать когда будет модель StoreProduct
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить товар
    """
    # TODO: Реализовать когда будет модель StoreProduct
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Функция в разработке"
    )


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
