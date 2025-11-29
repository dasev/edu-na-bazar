"""
Delivery Route model - оптимальные маршруты доставки
"""
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class DeliveryRoute(Base):
    """DeliveryRoute model - маршруты доставки заказов"""
    __tablename__ = "delivery_routes"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(BigInteger, ForeignKey('market.orders.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    
    # Точки маршрута (JSON массив с координатами и адресами)
    waypoints = Column(JSON, nullable=False)
    # [
    #   {"type": "store", "store_id": 1, "lat": 55.75, "lon": 37.61, "address": "..."},
    #   {"type": "store", "store_id": 2, "lat": 55.76, "lon": 37.62, "address": "..."},
    #   {"type": "customer", "lat": 55.77, "lon": 37.63, "address": "..."}
    # ]
    
    # Оптимизированный порядок посещения (индексы waypoints)
    optimized_order = Column(JSON, nullable=True)  # [0, 2, 1, 3]
    
    # Метрики маршрута
    total_distance = Column(Float, nullable=True)  # км
    total_duration = Column(Float, nullable=True)  # минуты
    
    # Геометрия маршрута (polyline от Yandex)
    route_geometry = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="delivery_route")
