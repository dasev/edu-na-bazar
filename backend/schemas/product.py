"""
Product schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID


# Request schemas
class ProductCreate(BaseModel):
    """Схема для создания товара"""
    name: str = Field(..., min_length=1, max_length=500)
    slug: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    old_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    image: Optional[str] = Field(None, max_length=500)
    images: Optional[List[str]] = None
    category_id: UUID
    rating: Decimal = Field(default=Decimal("0.0"), ge=0, le=5, decimal_places=2)
    reviews_count: int = Field(default=0, ge=0)
    in_stock: bool = True
    stock_quantity: int = Field(default=0, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)


class ProductUpdate(BaseModel):
    """Схема для обновления товара"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    slug: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    old_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    image: Optional[str] = Field(None, max_length=500)
    images: Optional[List[str]] = None
    category_id: Optional[UUID] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=5, decimal_places=2)
    reviews_count: Optional[int] = Field(None, ge=0)
    in_stock: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)


# Response schemas
class ProductResponse(BaseModel):
    """Схема ответа с товаром"""
    id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    old_price: Optional[Decimal]
    image: Optional[str]
    category_id: Optional[UUID]
    rating: Decimal
    reviews_count: int
    in_stock: bool
    unit: str
    created_at: datetime
    updated_at: datetime
    discount_percent: int = 0
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Схема ответа со списком товаров"""
    data: List[ProductResponse]
    meta: dict


# Filters
class ProductFilters(BaseModel):
    """Фильтры для товаров"""
    category_id: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    min_rating: Optional[Decimal] = None
    in_stock: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = Field(default="created_at", pattern="^(price|rating|created_at|name)$")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
