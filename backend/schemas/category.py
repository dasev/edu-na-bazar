"""
Category schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# Request schemas
class CategoryCreate(BaseModel):
    """Схема для создания категории"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)
    parent_id: Optional[str] = None
    sort_order: int = Field(default=0, ge=0)


class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)
    parent_id: Optional[str] = None
    sort_order: Optional[int] = Field(None, ge=0)


# Response schemas
class CategoryResponse(BaseModel):
    """Схема ответа с категорией"""
    id: UUID
    name: str
    slug: str
    icon: Optional[str]
    description: Optional[str]
    parent_id: Optional[UUID]
    sort_order: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryWithSubcategories(CategoryResponse):
    """Категория с подкатегориями"""
    subcategories: list[CategoryResponse] = []
    
    class Config:
        from_attributes = True
