"""
Store Owner model - магазины пользователей
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from database import Base


class StoreStatus(str, enum.Enum):
    """Статусы магазина"""
    PENDING = "pending"      # На модерации
    ACTIVE = "active"        # Активен
    SUSPENDED = "suspended"  # Приостановлен
    REJECTED = "rejected"    # Отклонен


class StoreOwner(Base):
    """Store Owner model - магазины пользователей"""
    __tablename__ = "store_owners"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Владелец
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Реквизиты
    inn = Column(String(12), nullable=False, unique=True, index=True)
    kpp = Column(String(9), nullable=True)
    ogrn = Column(String(15), nullable=True)
    
    # Названия
    name = Column(String(500), nullable=False)  # Короткое название
    legal_name = Column(String(1000), nullable=False)  # Полное юридическое название
    
    # Контакты
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Описание и медиа
    description = Column(Text, nullable=True)
    logo = Column(String(500), nullable=True)  # URL логотипа
    banner = Column(String(500), nullable=True)  # URL баннера
    
    # Статус
    status = Column(SQLEnum(StoreStatus), default=StoreStatus.PENDING, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", backref="owned_stores")
    
    def __repr__(self):
        return f"<StoreOwner {self.name} (ИНН: {self.inn})>"
