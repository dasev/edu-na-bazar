"""
Pydantic схемы для отзывов и вопросов
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


# ============= ОТЗЫВЫ =============

class ReviewCreate(BaseModel):
    """Создание отзыва"""
    product_id: int
    rating: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    title: Optional[str] = Field(None, max_length=200)
    comment: str = Field(..., min_length=10, description="Текст отзыва")
    advantages: Optional[str] = None
    disadvantages: Optional[str] = None


class ReviewResponse(BaseModel):
    """Отзыв для ответа"""
    id: int
    product_id: int
    user_id: Optional[int]
    rating: int
    title: Optional[str]
    comment: str
    advantages: Optional[str]
    disadvantages: Optional[str]
    is_verified_purchase: bool
    helpful_count: int
    not_helpful_count: int
    created_at: datetime
    updated_at: datetime
    
    # Вложенные данные
    user_name: Optional[str] = None
    seller_response: Optional[str] = None
    
    class Config:
        from_attributes = True


class ReviewVoteCreate(BaseModel):
    """Оценка полезности отзыва"""
    review_id: int
    is_helpful: bool


# ============= ВОПРОСЫ =============

class QuestionCreate(BaseModel):
    """Создание вопроса"""
    product_id: int
    question_text: str = Field(..., min_length=5, description="Текст вопроса")
    is_anonymous: bool = False


class AnswerCreate(BaseModel):
    """Создание ответа на вопрос"""
    question_id: int
    answer_text: str = Field(..., min_length=5, description="Текст ответа")


class AnswerResponse(BaseModel):
    """Ответ для отображения"""
    id: int
    answer_text: str
    is_seller: bool
    created_at: datetime
    user_name: Optional[str] = None
    store_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    """Вопрос для отображения"""
    id: int
    product_id: int
    question_text: str
    is_anonymous: bool
    helpful_count: int
    created_at: datetime
    
    # Вложенные данные
    user_name: Optional[str] = None
    answers: List[AnswerResponse] = []
    
    class Config:
        from_attributes = True


# ============= ОТВЕТЫ ПРОДАВЦА =============

class ReviewResponseCreate(BaseModel):
    """Ответ продавца на отзыв"""
    review_id: int
    response_text: str = Field(..., min_length=10)


class ReviewResponseSchema(BaseModel):
    """Ответ продавца для отображения"""
    id: int
    response_text: str
    created_at: datetime
    store_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============= СТАТИСТИКА =============

class ReviewStats(BaseModel):
    """Статистика отзывов о товаре"""
    total_reviews: int
    average_rating: float
    rating_distribution: dict  # {5: 10, 4: 5, 3: 2, 2: 1, 1: 0}
    verified_purchases: int
