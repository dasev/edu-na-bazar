"""
Cart schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# Request schemas
class CartItemCreate(BaseModel):
    """Схема для добавления товара в корзину"""
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    """Схема для обновления товара в корзине"""
    quantity: int = Field(..., gt=0)


# Response schemas
class CartItemResponse(BaseModel):
    """Схема ответа с товаром в корзине"""
    id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    # Информация о товаре (join)
    product_name: Optional[str] = None
    product_price: Optional[Decimal] = None
    product_image: Optional[str] = None
    product_in_stock: Optional[bool] = None
    subtotal: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Схема ответа с корзиной"""
    items: List[CartItemResponse]
    total: Decimal
    items_count: int
