"""
Store model (with PostGIS)
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, BigInteger, Text
from geoalchemy2 import Geometry
from database import Base


class Store(Base):
    """Store model - магазины с геолокацией (PostGIS)"""
    __tablename__ = "stores"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Основная информация
    name = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=False)
    phone = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    
    # Время работы
    working_hours = Column(Text, nullable=True)  # Например: "8:00 - 22:00"
    
    
    # Геолокация (PostGIS)
    # POINT - координаты магазина (долгота, широта)
    # SRID 4326 - стандарт WGS84 (используется в GPS, Google Maps, Mapbox)
    location = Column(Geometry('POINT', srid=4326), nullable=True)
    
    # Зона доставки (PostGIS)
    # POLYGON - полигон зоны доставки
    delivery_zone = Column(Geometry('POLYGON', srid=4326), nullable=True)
    
    # Изображение
    image = Column(Text, nullable=True)
    
    # Статус
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Store {self.name} - {self.address}>"
