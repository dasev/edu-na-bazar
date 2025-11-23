"""
Store model (with PostGIS)
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from database import Base


class Store(Base):
    """Store model - магазины с геолокацией (PostGIS)"""
    __tablename__ = "stores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Основная информация
    name = Column(String(255), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Время работы
    working_hours = Column(String(255), nullable=True)  # Например: "8:00 - 22:00"
    
    # Описание
    description = Column(Text, nullable=True)
    
    # Геолокация (PostGIS)
    # POINT - координаты магазина (долгота, широта)
    # SRID 4326 - стандарт WGS84 (используется в GPS, Google Maps, Mapbox)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    # Зона доставки (PostGIS)
    # POLYGON - полигон зоны доставки
    delivery_zone = Column(Geometry('POLYGON', srid=4326), nullable=True)
    
    # Изображение
    image = Column(String(500), nullable=True)
    
    # Статус
    is_active = Column(String(10), default="true")  # true/false как строка для совместимости
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Store {self.name} - {self.address}>"
