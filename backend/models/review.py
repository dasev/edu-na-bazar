"""
Модели для отзывов и вопросов о товарах
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey, BigInteger, Integer, Boolean, String
from sqlalchemy.orm import relationship
from database import Base


class ProductReview(Base):
    """Отзывы о товарах"""
    __tablename__ = "product_reviews"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='SET NULL'), nullable=True, index=True)
    
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=False)
    advantages = Column(Text, nullable=True)
    disadvantages = Column(Text, nullable=True)
    
    is_verified_purchase = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="product_reviews")
    user = relationship("User", back_populates="product_reviews")
    responses = relationship("ReviewResponse", back_populates="review", cascade="all, delete-orphan")
    votes = relationship("ReviewVote", back_populates="review", cascade="all, delete-orphan")


class ReviewResponse(Base):
    """Ответы продавца на отзывы"""
    __tablename__ = "review_responses"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    review_id = Column(BigInteger, ForeignKey('market.product_reviews.id', ondelete='CASCADE'), nullable=False)
    store_id = Column(BigInteger, ForeignKey('market.stores.id', ondelete='CASCADE'), nullable=True)
    response_text = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    review = relationship("ProductReview", back_populates="responses")
    store = relationship("Store")


class ProductQuestion(Base):
    """Вопросы о товарах"""
    __tablename__ = "product_questions"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='SET NULL'), nullable=True, index=True)
    
    question_text = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="product_questions")
    user = relationship("User", back_populates="product_questions")
    answers = relationship("QuestionAnswer", back_populates="question", cascade="all, delete-orphan")


class QuestionAnswer(Base):
    """Ответы на вопросы"""
    __tablename__ = "question_answers"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey('market.product_questions.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='SET NULL'), nullable=True)
    store_id = Column(BigInteger, ForeignKey('market.stores.id', ondelete='CASCADE'), nullable=True)
    
    answer_text = Column(Text, nullable=False)
    is_seller = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    question = relationship("ProductQuestion", back_populates="answers")
    user = relationship("User")
    store = relationship("Store")


class ReviewVote(Base):
    """Оценки полезности отзывов"""
    __tablename__ = "review_votes"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    review_id = Column(BigInteger, ForeignKey('market.product_reviews.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='CASCADE'), nullable=False)
    is_helpful = Column(Boolean, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    review = relationship("ProductReview", back_populates="votes")
    user = relationship("User")
