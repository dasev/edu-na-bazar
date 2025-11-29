"""
Product Views API - отслеживание просмотров товаров
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.product_view import ProductView
from models.user import User
from api.dependencies import get_current_user_optional
import uuid

router = APIRouter(prefix="/api/product-views", tags=["product-views"])


@router.post("/{product_id}")
async def track_product_view(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """Записать просмотр товара"""
    
    # Получаем session_id из cookies или создаем новый
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Создаем запись о просмотре
    view = ProductView(
        product_id=product_id,
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    db.add(view)
    await db.commit()
    
    return {"status": "ok", "session_id": session_id}
