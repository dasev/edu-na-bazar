"""
API для отзывов и вопросов о товарах
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from database import get_db
from models.review import ProductReview, ReviewResponse as ReviewResponseModel, ProductQuestion, QuestionAnswer, ReviewVote
from models.product import Product
from models.user import User
from models.store import Store
from schemas.review import (
    ReviewCreate, ReviewResponse, ReviewVoteCreate,
    QuestionCreate, QuestionResponse, AnswerCreate, AnswerResponse,
    ReviewResponseCreate, ReviewResponseSchema, ReviewStats
)
from api.dependencies import get_current_user, get_current_user_optional

router = APIRouter(prefix="/reviews", tags=["reviews"])


# ============= ОТЗЫВЫ =============

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: int,
    skip: int = 0,
    limit: int = 20,
    rating: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Получить отзывы о товаре"""
    query = select(ProductReview).where(ProductReview.product_id == product_id)
    
    if rating:
        query = query.where(ProductReview.rating == rating)
    
    query = query.order_by(ProductReview.created_at.desc()).offset(skip).limit(limit)
    query = query.options(selectinload(ProductReview.user), selectinload(ProductReview.responses))
    
    result = await db.execute(query)
    reviews = result.scalars().all()
    
    # Формируем ответ
    response_data = []
    for review in reviews:
        review_dict = {
            "id": review.id,
            "product_id": review.product_id,
            "user_id": review.user_id,
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "advantages": review.advantages,
            "disadvantages": review.disadvantages,
            "is_verified_purchase": review.is_verified_purchase,
            "helpful_count": review.helpful_count,
            "not_helpful_count": review.not_helpful_count,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "user_name": (review.user.full_name or review.user.email) if review.user else "Аноним",
            "seller_response": review.responses[0].response_text if review.responses else None
        }
        response_data.append(review_dict)
    
    return response_data


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать отзыв"""
    # Проверяем существование товара
    result = await db.execute(select(Product).where(Product.id == review_data.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Проверяем, не оставлял ли пользователь уже отзыв
    result = await db.execute(
        select(ProductReview).where(
            and_(
                ProductReview.product_id == review_data.product_id,
                ProductReview.user_id == current_user.id
            )
        )
    )
    existing_review = result.scalar_one_or_none()
    if existing_review:
        raise HTTPException(status_code=400, detail="Вы уже оставили отзыв на этот товар")
    
    # Создаем отзыв
    new_review = ProductReview(
        product_id=review_data.product_id,
        user_id=current_user.id,
        rating=review_data.rating,
        title=review_data.title,
        comment=review_data.comment,
        advantages=review_data.advantages,
        disadvantages=review_data.disadvantages,
        is_verified_purchase=False  # TODO: проверить покупку
    )
    
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    
    # Обновляем рейтинг товара
    await update_product_rating(product.id, db)
    
    return {
        **new_review.__dict__,
        "user_name": current_user.full_name or current_user.email,
        "seller_response": None
    }


@router.post("/vote", status_code=status.HTTP_201_CREATED)
async def vote_review(
    vote_data: ReviewVoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Оценить полезность отзыва"""
    # Проверяем существование отзыва
    result = await db.execute(select(ProductReview).where(ProductReview.id == vote_data.review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    # Проверяем, не голосовал ли уже
    result = await db.execute(
        select(ReviewVote).where(
            and_(
                ReviewVote.review_id == vote_data.review_id,
                ReviewVote.user_id == current_user.id
            )
        )
    )
    existing_vote = result.scalar_one_or_none()
    
    if existing_vote:
        # Обновляем голос
        if existing_vote.is_helpful != vote_data.is_helpful:
            if existing_vote.is_helpful:
                review.helpful_count -= 1
                review.not_helpful_count += 1
            else:
                review.not_helpful_count -= 1
                review.helpful_count += 1
            existing_vote.is_helpful = vote_data.is_helpful
    else:
        # Создаем новый голос
        new_vote = ReviewVote(
            review_id=vote_data.review_id,
            user_id=current_user.id,
            is_helpful=vote_data.is_helpful
        )
        db.add(new_vote)
        
        if vote_data.is_helpful:
            review.helpful_count += 1
        else:
            review.not_helpful_count += 1
    
    await db.commit()
    
    return {"message": "Голос учтен"}


@router.get("/product/{product_id}/stats", response_model=ReviewStats)
async def get_review_stats(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику отзывов"""
    # Общее количество
    result = await db.execute(
        select(func.count(ProductReview.id)).where(ProductReview.product_id == product_id)
    )
    total = result.scalar()
    
    # Средний рейтинг
    result = await db.execute(
        select(func.avg(ProductReview.rating)).where(ProductReview.product_id == product_id)
    )
    avg_rating = result.scalar() or 0.0
    
    # Распределение по рейтингам
    rating_dist = {}
    for rating in range(1, 6):
        result = await db.execute(
            select(func.count(ProductReview.id)).where(
                and_(
                    ProductReview.product_id == product_id,
                    ProductReview.rating == rating
                )
            )
        )
        rating_dist[rating] = result.scalar()
    
    # Подтвержденные покупки
    result = await db.execute(
        select(func.count(ProductReview.id)).where(
            and_(
                ProductReview.product_id == product_id,
                ProductReview.is_verified_purchase == True
            )
        )
    )
    verified = result.scalar()
    
    return {
        "total_reviews": total,
        "average_rating": round(avg_rating, 1),
        "rating_distribution": rating_dist,
        "verified_purchases": verified
    }


# ============= ВОПРОСЫ =============

@router.get("/questions/product/{product_id}", response_model=List[QuestionResponse])
async def get_product_questions(
    product_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Получить вопросы о товаре"""
    query = select(ProductQuestion).where(ProductQuestion.product_id == product_id)
    query = query.order_by(ProductQuestion.created_at.desc()).offset(skip).limit(limit)
    query = query.options(
        selectinload(ProductQuestion.user),
        selectinload(ProductQuestion.answers).selectinload(QuestionAnswer.user),
        selectinload(ProductQuestion.answers).selectinload(QuestionAnswer.store)
    )
    
    result = await db.execute(query)
    questions = result.scalars().all()
    
    # Формируем ответ
    response_data = []
    for question in questions:
        answers_data = []
        for answer in question.answers:
            user_name = None
            if answer.user:
                user_name = answer.user.full_name or answer.user.email
            
            answers_data.append({
                "id": answer.id,
                "answer_text": answer.answer_text,
                "is_seller": answer.is_seller,
                "created_at": answer.created_at,
                "user_name": user_name,
                "store_name": answer.store.name if answer.store else None
            })
        
        user_display_name = "Аноним"
        if not question.is_anonymous and question.user:
            user_display_name = question.user.full_name or question.user.email or "Пользователь"
        
        question_dict = {
            "id": question.id,
            "product_id": question.product_id,
            "question_text": question.question_text,
            "is_anonymous": question.is_anonymous,
            "helpful_count": question.helpful_count,
            "created_at": question.created_at,
            "user_name": user_display_name,
            "answers": answers_data
        }
        response_data.append(question_dict)
    
    return response_data


@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """Создать вопрос"""
    # Проверяем существование товара
    result = await db.execute(select(Product).where(Product.id == question_data.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Создаем вопрос
    new_question = ProductQuestion(
        product_id=question_data.product_id,
        user_id=current_user.id if current_user else None,
        question_text=question_data.question_text,
        is_anonymous=question_data.is_anonymous
    )
    
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    
    return {
        "id": new_question.id,
        "product_id": new_question.product_id,
        "question_text": new_question.question_text,
        "is_anonymous": new_question.is_anonymous,
        "helpful_count": 0,
        "created_at": new_question.created_at,
        "user_name": "Аноним" if new_question.is_anonymous else ((current_user.full_name or current_user.email) if current_user else "Аноним"),
        "answers": []
    }


@router.post("/questions/answer", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def answer_question(
    answer_data: AnswerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Ответить на вопрос"""
    # Проверяем существование вопроса
    result = await db.execute(select(ProductQuestion).where(ProductQuestion.id == answer_data.question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    # Создаем ответ
    new_answer = QuestionAnswer(
        question_id=answer_data.question_id,
        user_id=current_user.id,
        answer_text=answer_data.answer_text,
        is_seller=False  # TODO: проверить является ли продавцом
    )
    
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    
    return {
        "id": new_answer.id,
        "answer_text": new_answer.answer_text,
        "is_seller": new_answer.is_seller,
        "created_at": new_answer.created_at,
        "user_name": current_user.full_name or current_user.email,
        "store_name": None
    }


# ============= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =============

async def update_product_rating(product_id: int, db: AsyncSession):
    """Обновить рейтинг товара"""
    # Считаем средний рейтинг
    result = await db.execute(
        select(func.avg(ProductReview.rating), func.count(ProductReview.id))
        .where(ProductReview.product_id == product_id)
    )
    avg_rating, count = result.one()
    
    # Обновляем товар
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one()
    product.rating = round(avg_rating, 1) if avg_rating else 0.0
    product.reviews_count = count
    
    await db.commit()
