"""
User Event model - отслеживание микро-конверсий и событий пользователей
"""
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class UserEvent(Base):
    """UserEvent model - события пользователей для аналитики"""
    __tablename__ = "user_events"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)
    
    # Тип события
    event_type = Column(String(50), nullable=False, index=True)
    # Типы: 'product_click', 'add_to_cart_click', 'checkout_start', 'checkout_complete'
    
    # Связанные объекты
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='SET NULL'), nullable=True, index=True)
    order_id = Column(BigInteger, ForeignKey('market.orders.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Дополнительные данные (JSON)
    event_data = Column(Text, nullable=True)  # JSON строка с доп. данными
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="events")
    product = relationship("Product")
    order = relationship("Order")
