"""
Geography models - регионы и города
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey, BigInteger, Double
from sqlalchemy.orm import relationship
from database import Base


class Region(Base):
    """Region model - регионы РФ"""
    __tablename__ = "regions"
    __table_args__ = {'schema': 'geo'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Информация
    name = Column(Text, nullable=False, index=True)
    code = Column(Text, unique=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cities = relationship("City", back_populates="region")
    
    def __repr__(self):
        return f"<Region {self.name} ({self.code})>"


class City(Base):
    """City model - города РФ"""
    __tablename__ = "cities"
    __table_args__ = {'schema': 'geo'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Связи
    region_id = Column(BigInteger, ForeignKey('geo.regions.id'), nullable=True, index=True)
    
    # Информация
    name = Column(Text, nullable=False, index=True)
    
    # Координаты
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    region = relationship("Region", back_populates="cities")
    
    def __repr__(self):
        return f"<City {self.name} - Region {self.region_id}>"
