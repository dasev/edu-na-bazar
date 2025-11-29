"""
Order models
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, Text, Double
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    """Order model - заказы"""
    __tablename__ = "orders"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Пользователь
    user_id = Column(BigInteger, ForeignKey('config.users.id'), nullable=False, index=True)
    
    # Магазин (если есть)
    store_id = Column(BigInteger, nullable=True)
    
    # Сумма (в БД называется total_amount)
    total_amount = Column(Double, nullable=False)
    
    # Статус заказа
    # pending - ожидает
    # created - создан
    # paid - оплачен
    # processing - в обработке
    # delivering - доставляется
    # completed - выполнен
    # cancelled - отменен
    status = Column(Text, default="pending", nullable=False, index=True)
    
    # Доставка
    delivery_address = Column(Text, nullable=False)
    delivery_phone = Column(Text, nullable=False)  # В БД delivery_phone
    
    # Оплата
    payment_method = Column(Text, nullable=False)  # card, cash, online
    
    # Комментарий (в БД называется notes)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    delivery_route = relationship("DeliveryRoute", back_populates="order", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        try:
            return f"<Order {self.id} - {self.status} - {self.total_amount}₽>"
        except:
            return f"<Order (detached)>"


class OrderItem(Base):
    """OrderItem model - товары в заказе"""
    __tablename__ = "order_items"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Заказ
    order_id = Column(BigInteger, ForeignKey('market.orders.id'), nullable=False, index=True)
    
    # Товар
    product_id = Column(BigInteger, ForeignKey('market.products.id'), nullable=False)
    
    # Количество и цена (фиксируем на момент заказа)
    quantity = Column(BigInteger, nullable=False)
    price = Column(Double, nullable=False)  # Цена на момент заказа
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem product_id={self.product_id} x{self.quantity}>"
    
    @property
    def subtotal(self):
        """Подытог для этого товара"""
        return float(self.price) * self.quantity
