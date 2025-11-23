"""
Order models
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy.orm import relationship
import uuid
from database import Base


class Order(Base):
    """Order model - заказы"""
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Пользователь
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Статус заказа
    # created - создан
    # paid - оплачен
    # processing - в обработке
    # delivering - доставляется
    # completed - выполнен
    # cancelled - отменен
    status = Column(String(50), default="created", nullable=False, index=True)
    
    # Сумма
    total = Column(NUMERIC(10, 2), nullable=False)
    
    # Доставка
    delivery_address = Column(String(500), nullable=False)
    delivery_time = Column(DateTime, nullable=True)  # Желаемое время доставки
    delivery_comment = Column(Text, nullable=True)
    
    # Оплата
    payment_method = Column(String(50), nullable=False)  # card, cash, online
    payment_status = Column(String(50), default="pending")  # pending, paid, failed
    
    # Контакты
    contact_phone = Column(String(20), nullable=False)
    contact_name = Column(String(255), nullable=False)
    
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
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Заказ
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False, index=True)
    
    # Товар
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    
    # Количество и цена (фиксируем на момент заказа)
    quantity = Column(Integer, nullable=False)
    price = Column(NUMERIC(10, 2), nullable=False)  # Цена на момент заказа
    
    # Название товара (на случай если товар удалят)
    product_name = Column(String(500), nullable=False)
    product_image = Column(String(500), nullable=True)
    
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
