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
    
    # Статус заказа
    # created - создан
    # paid - оплачен
    # processing - в обработке
    # delivering - доставляется
    # completed - выполнен
    # cancelled - отменен
    status = Column(Text, default="created", nullable=False, index=True)
    
    # Сумма
    total = Column(Double, nullable=False)
    
    # Доставка
    delivery_address = Column(Text, nullable=False)
    delivery_time = Column(DateTime, nullable=True)  # Желаемое время доставки
    delivery_comment = Column(Text, nullable=True)
    
    # Оплата
    payment_method = Column(Text, nullable=False)  # card, cash, online
    payment_status = Column(Text, default="pending")  # pending, paid, failed
    
    # Контакты
    contact_phone = Column(Text, nullable=False)
    contact_name = Column(Text, nullable=False)
    
    # Комментарий
    comment = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order {self.id} - {self.status} - {self.total}₽>"


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
    
    # Название товара (на случай если товар удалят)
    product_name = Column(Text, nullable=False)
    product_image = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem {self.product_name} x{self.quantity}>"
    
    @property
    def subtotal(self):
        """Подытог для этого товара"""
        return float(self.price) * self.quantity
