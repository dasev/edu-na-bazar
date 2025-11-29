import { useState, useEffect } from 'react'
import { Tabs } from 'devextreme-react/tabs'
import { Button } from 'devextreme-react/button'
import { TextArea } from 'devextreme-react/text-area'
import { apiClient } from '../../api/client'
import { showToast } from '../../utils/toast'
import './ProductReviews.css'

interface Review {
  id: number
  rating: number
  title: string
  comment: string
  advantages: string | null
  disadvantages: string | null
  user_name: string
  created_at: string
  helpful_count: number
  not_helpful_count: number
  seller_response: string | null
  is_verified_purchase: boolean
}

interface Question {
  id: number
  question_text: string
  user_name: string
  created_at: string
  answers: Array<{
    id: number
    answer_text: string
    is_seller: boolean
    user_name: string | null
    store_name: string | null
    created_at: string
  }>
}

interface ProductReviewsProps {
  productId: number
}

export default function ProductReviews({ productId }: ProductReviewsProps) {
  const [activeTab, setActiveTab] = useState(0)
  const [reviews, setReviews] = useState<Review[]>([])
  const [questions, setQuestions] = useState<Question[]>([])
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  
  // Форма отзыва
  const [showReviewForm, setShowReviewForm] = useState(false)
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    title: '',
    comment: '',
    advantages: '',
    disadvantages: ''
  })
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})
  
  // Форма вопроса
  const [showQuestionForm, setShowQuestionForm] = useState(false)
  const [questionText, setQuestionText] = useState('')

  const tabs = [
    { id: 0, text: `Отзывы о товаре ${stats?.total_reviews || 0}` },
    { id: 1, text: `Вопросы о товаре ${questions.length}` }
  ]

  useEffect(() => {
    loadReviews()
    loadQuestions()
    loadStats()
  }, [productId])

  const loadReviews = async () => {
    try {
      const response = await apiClient.get(`/api/reviews/product/${productId}`)
      setReviews(response.data)
    } catch (error) {
      console.error('Error loading reviews:', error)
    }
  }

  const loadQuestions = async () => {
    try {
      const response = await apiClient.get(`/api/reviews/questions/product/${productId}`)
      setQuestions(response.data)
    } catch (error) {
      console.error('Error loading questions:', error)
    }
  }

  const loadStats = async () => {
    try {
      const response = await apiClient.get(`/api/reviews/product/${productId}/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const handleSubmitReview = async () => {
    // Очищаем предыдущие ошибки
    setValidationErrors({})

    if (!reviewForm.comment.trim()) {
      setValidationErrors({ comment: 'Напишите отзыв' })
      showToast.error('Напишите отзыв')
      return
    }

    setLoading(true)
    try {
      await apiClient.post('/api/reviews/', {
        product_id: productId,
        ...reviewForm
      })
      showToast.success('Отзыв добавлен!')
      setShowReviewForm(false)
      setReviewForm({ rating: 5, title: '', comment: '', advantages: '', disadvantages: '' })
      setValidationErrors({})
      loadReviews()
      loadStats()
    } catch (error: any) {
      // Обработка ошибок валидации от backend
      if (error.response?.data?.error === 'ValidationError' && error.response?.data?.details) {
        const errors: Record<string, string> = {}
        const details = error.response.data.details
        
        details.forEach((detail: any) => {
          const field = detail.loc[detail.loc.length - 1] // Последний элемент в loc - это имя поля
          let message = detail.msg
          
          // Переводим сообщения на русский
          if (detail.type === 'string_too_short') {
            const minLength = detail.ctx?.min_length || 10
            message = `Минимальная длина: ${minLength} символов`
          } else if (detail.type === 'string_too_long') {
            const maxLength = detail.ctx?.max_length
            message = `Максимальная длина: ${maxLength} символов`
          } else if (detail.type === 'value_error') {
            message = 'Некорректное значение'
          }
          
          errors[field] = message
        })
        
        setValidationErrors(errors)
        
        // Показываем первую ошибку
        const firstError = Object.entries(errors)[0]
        if (firstError) {
          const fieldNames: Record<string, string> = {
            comment: 'Комментарий',
            title: 'Заголовок',
            advantages: 'Достоинства',
            disadvantages: 'Недостатки'
          }
          showToast.error(`${fieldNames[firstError[0]] || firstError[0]}: ${firstError[1]}`)
        }
      } else {
        showToast.error(error.response?.data?.detail || 'Ошибка при добавлении отзыва')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitQuestion = async () => {
    if (!questionText.trim()) {
      showToast.error('Напишите вопрос')
      return
    }

    setLoading(true)
    try {
      await apiClient.post('/api/reviews/questions', {
        product_id: productId,
        question_text: questionText,
        is_anonymous: false
      })
      showToast.success('Вопрос добавлен!')
      setShowQuestionForm(false)
      setQuestionText('')
      loadQuestions()
    } catch (error: any) {
      showToast.error(error.response?.data?.detail || 'Ошибка при добавлении вопроса')
    } finally {
      setLoading(false)
    }
  }

  const handleVoteReview = async (reviewId: number, isHelpful: boolean) => {
    try {
      await apiClient.post('/api/reviews/vote', {
        review_id: reviewId,
        is_helpful: isHelpful
      })
      showToast.success('Спасибо за оценку!')
      loadReviews()
    } catch (error: any) {
      showToast.error(error.response?.data?.detail || 'Ошибка')
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
  }

  const renderStars = (rating: number) => {
    return (
      <div className="stars">
        {[1, 2, 3, 4, 5].map(star => (
          <span key={star} className={star <= rating ? 'star filled' : 'star'}>★</span>
        ))}
      </div>
    )
  }

  return (
    <div className="product-reviews">
      <Tabs
        dataSource={tabs}
        selectedIndex={activeTab}
        onItemClick={(e) => {
          setActiveTab(e.itemIndex)
        }}
      />

      <div className="product-reviews__content">
        {activeTab === 0 ? (
          <div className="reviews-tab">
            {/* Статистика */}
            {stats && (
              <div className="reviews-stats">
                <div className="reviews-stats__summary">
                  <div className="reviews-stats__rating">
                    <div className="rating-number">{stats.average_rating}</div>
                    {renderStars(Math.round(stats.average_rating))}
                    <div className="rating-count">{stats.total_reviews} отзывов</div>
                  </div>
                  
                  <div className="reviews-stats__distribution">
                    {[5, 4, 3, 2, 1].map(rating => (
                      <div key={rating} className="rating-bar">
                        <span className="rating-label">{rating} ★</span>
                        <div className="rating-progress">
                          <div 
                            className="rating-progress-fill"
                            style={{ 
                              width: `${stats.total_reviews > 0 ? (stats.rating_distribution[rating] / stats.total_reviews * 100) : 0}%` 
                            }}
                          />
                        </div>
                        <span className="rating-count">{stats.rating_distribution[rating]}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <Button
                  text="Написать отзыв"
                  type="default"
                  onClick={() => setShowReviewForm(!showReviewForm)}
                />
              </div>
            )}

            {/* Форма отзыва */}
            {showReviewForm && (
              <div className="review-form">
                <h3>Ваш отзыв</h3>
                
                <div className="form-group">
                  <label>Оценка</label>
                  <div className="rating-input">
                    {[1, 2, 3, 4, 5].map(star => (
                      <span
                        key={star}
                        className={star <= reviewForm.rating ? 'star filled clickable' : 'star clickable'}
                        onClick={() => setReviewForm({ ...reviewForm, rating: star })}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label>Заголовок (необязательно)</label>
                  <input
                    type="text"
                    value={reviewForm.title}
                    onChange={(e) => setReviewForm({ ...reviewForm, title: e.target.value })}
                    placeholder="Краткое резюме"
                    className={validationErrors.title ? 'input-error' : ''}
                  />
                  {validationErrors.title && (
                    <div className="error-message">{validationErrors.title}</div>
                  )}
                </div>

                <div className="form-group">
                  <label>Комментарий * <span className="field-hint">(минимум 10 символов)</span></label>
                  <TextArea
                    value={reviewForm.comment}
                    onValueChanged={(e) => setReviewForm({ ...reviewForm, comment: e.value })}
                    placeholder="Расскажите о товаре подробнее (минимум 10 символов)"
                    height={100}
                    className={validationErrors.comment ? 'textarea-error' : ''}
                  />
                  {validationErrors.comment && (
                    <div className="error-message">{validationErrors.comment}</div>
                  )}
                </div>

                <div className="form-group">
                  <label>Достоинства</label>
                  <TextArea
                    value={reviewForm.advantages}
                    onValueChanged={(e) => setReviewForm({ ...reviewForm, advantages: e.value })}
                    height={60}
                    className={validationErrors.advantages ? 'textarea-error' : ''}
                  />
                  {validationErrors.advantages && (
                    <div className="error-message">{validationErrors.advantages}</div>
                  )}
                </div>

                <div className="form-group">
                  <label>Недостатки</label>
                  <TextArea
                    value={reviewForm.disadvantages}
                    onValueChanged={(e) => setReviewForm({ ...reviewForm, disadvantages: e.value })}
                    height={60}
                    className={validationErrors.disadvantages ? 'textarea-error' : ''}
                  />
                  {validationErrors.disadvantages && (
                    <div className="error-message">{validationErrors.disadvantages}</div>
                  )}
                </div>

                <div className="form-actions">
                  <Button text="Отправить" type="default" onClick={handleSubmitReview} disabled={loading} />
                  <Button text="Отмена" type="normal" onClick={() => setShowReviewForm(false)} />
                </div>
              </div>
            )}

            {/* Список отзывов */}
            <div className="reviews-list">
              {reviews.map(review => (
                <div key={review.id} className="review-item">
                  <div className="review-header">
                    <div className="review-user">
                      <div className="user-avatar">{review.user_name[0]}</div>
                      <div>
                        <div className="user-name">{review.user_name}</div>
                        <div className="review-date">{formatDate(review.created_at)}</div>
                      </div>
                    </div>
                    {renderStars(review.rating)}
                  </div>

                  {review.title && <h4 className="review-title">{review.title}</h4>}
                  
                  <p className="review-comment">{review.comment}</p>

                  {review.advantages && (
                    <div className="review-section">
                      <strong>Достоинства:</strong> {review.advantages}
                    </div>
                  )}

                  {review.disadvantages && (
                    <div className="review-section">
                      <strong>Недостатки:</strong> {review.disadvantages}
                    </div>
                  )}

                  {review.is_verified_purchase && (
                    <div className="verified-badge">✓ Подтвержденная покупка</div>
                  )}

                  {review.seller_response && (
                    <div className="seller-response">
                      <strong>Ответ продавца:</strong>
                      <p>{review.seller_response}</p>
                    </div>
                  )}

                  <div className="review-actions">
                    <span>Вам помог этот отзыв?</span>
                    <Button
                      text={`Да ${review.helpful_count}`}
                      stylingMode="text"
                      onClick={() => handleVoteReview(review.id, true)}
                    />
                    <Button
                      text={`Нет ${review.not_helpful_count}`}
                      stylingMode="text"
                      onClick={() => handleVoteReview(review.id, false)}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="questions-tab">
            <div style={{ marginBottom: '20px' }}>
              <Button
                text="Задать вопрос"
                type="default"
                onClick={() => setShowQuestionForm(!showQuestionForm)}
              />
            </div>

            {/* Форма вопроса */}
            {showQuestionForm && (
              <div className="question-form">
                <h3>Задайте вопрос о товаре</h3>
                <TextArea
                  value={questionText}
                  onValueChanged={(e) => setQuestionText(e.value)}
                  placeholder="Напишите свой вопрос"
                  height={100}
                />
                <div className="form-actions">
                  <Button text="Отправить" type="default" onClick={handleSubmitQuestion} disabled={loading} />
                  <Button text="Отмена" type="normal" onClick={() => setShowQuestionForm(false)} />
                </div>
              </div>
            )}

            {/* Список вопросов */}
            <div className="questions-list">
              {questions.map(question => (
                <div key={question.id} className="question-item">
                  <div className="question-header">
                    <div className="user-avatar">{question.user_name[0]}</div>
                    <div>
                      <div className="user-name">{question.user_name}</div>
                      <div className="question-date">{formatDate(question.created_at)}</div>
                    </div>
                  </div>

                  <p className="question-text">{question.question_text}</p>

                  {question.answers.length > 0 && (
                    <div className="answers-list">
                      {question.answers.map(answer => (
                        <div key={answer.id} className="answer-item">
                          <div className="answer-header">
                            {answer.is_seller && <span className="seller-badge">Продавец</span>}
                            <span className="answer-author">
                              {answer.store_name || answer.user_name}
                            </span>
                            <span className="answer-date">{formatDate(answer.created_at)}</span>
                          </div>
                          <p className="answer-text">{answer.answer_text}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
