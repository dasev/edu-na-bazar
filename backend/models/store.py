"""
Store model (with PostGIS)
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import uuid
from database import Base
from models.enums import StoreStatus


class Store(Base):
    """Store model - магазины с геолокацией (PostGIS)"""
    __tablename__ = "stores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Владелец магазина
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Основная информация
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)  # URL-friendly имя
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Время работы
    working_hours = Column(String(255), nullable=True)  # Например: "8:00 - 22:00"
    
    # Геолокация (PostGIS)
    # POINT - координаты магазина (долгота, широта)
    # SRID 4326 - стандарт WGS84 (используется в GPS, Google Maps, Mapbox)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    # Зона доставки (PostGIS)
    # POLYGON - полигон зоны доставки
    delivery_zone = Column(Geometry('POLYGON', srid=4326), nullable=True)
    
    # Изображения
    logo = Column(String(500), nullable=True)
    banner = Column(String(500), nullable=True)
    
    # Рейтинг и статистика
    rating = Column(NUMERIC(3, 2), default=0.0)
    reviews_count = Column(Integer, default=0)
    products_count = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)
    
    # Статус модерации
    status = Column(Enum(StoreStatus), default=StoreStatus.PENDING, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="stores")
    products = relationship("Product", back_populates="store")
    
    def __repr__(self):
        return f"<Store {self.name} - {self.owner_id}>"
