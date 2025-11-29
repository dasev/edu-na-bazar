"""
Events API - отслеживание событий пользователей
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database import get_db
from models.user_event import UserEvent
from models.user import User
from api.dependencies import get_current_user_optional
import uuid

router = APIRouter(prefix="/api/events", tags=["events"])


class EventCreate(BaseModel):
    event_type: str  # 'product_click', 'add_to_cart_click', 'checkout_start', 'checkout_complete'
    product_id: int | None = None
    order_id: int | None = None
    event_data: str | None = None


@router.post("/track")
async def track_event(
    event: EventCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """Записать событие пользователя"""
    
    # Получаем session_id из cookies или создаем новый
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Создаем запись о событии
    user_event = UserEvent(
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        event_type=event.event_type,
        product_id=event.product_id,
        order_id=event.order_id,
        event_data=event.event_data
    )
    
    db.add(user_event)
    await db.commit()
    
    return {"status": "ok", "session_id": session_id}
