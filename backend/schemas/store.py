"""
Store schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Request schemas
class StoreCreate(BaseModel):
    """Схема для создания магазина"""
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    working_hours: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    image: Optional[str] = Field(None, max_length=500)
    is_active: str = "true"


class StoreUpdate(BaseModel):
    """Схема для обновления магазина"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    working_hours: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    image: Optional[str] = Field(None, max_length=500)
    is_active: Optional[str] = None


# Response schemas
class LocationResponse(BaseModel):
    """Координаты точки"""
    type: str = "Point"
    coordinates: list[float]  # [longitude, latitude]


class StoreResponse(BaseModel):
    """Схема ответа с магазином"""
    id: str
    name: str
    address: str
    phone: Optional[str]
    email: Optional[str]
    working_hours: Optional[str]
    description: Optional[str]
    location: LocationResponse
    image: Optional[str]
    is_active: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StoreNearbyRequest(BaseModel):
    """Запрос для поиска ближайших магазинов"""
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")
    radius_km: float = Field(default=5, ge=0.1, le=50, description="Радиус поиска в км")


class StoreWithDistance(StoreResponse):
    """Магазин с расстоянием"""
    distance_km: float = Field(..., description="Расстояние в км")
