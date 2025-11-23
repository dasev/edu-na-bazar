"""
Store Owner model - магазины пользователей
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base


class StoreOwner(Base):
    """Store Owner model - магазины пользователей"""
    __tablename__ = "store_owners"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Владелец
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Реквизиты
    inn = Column(Text, nullable=False, unique=True, index=True)
    kpp = Column(Text, nullable=True)
    ogrn = Column(Text, nullable=True)
    
    # Названия
    name = Column(Text, nullable=False)
    legal_name = Column(Text, nullable=False)
    
    # Контакты
    address = Column(Text, nullable=False)
    phone = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    
    # Описание и медиа
    description = Column(Text, nullable=True)
    logo = Column(Text, nullable=True)
    banner = Column(Text, nullable=True)
    
    # Статус
    status = Column(Text, default='pending', nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", backref="owned_stores")
    
    def __repr__(self):
        return f"<StoreOwner {self.name} (ИНН: {self.inn})>"
