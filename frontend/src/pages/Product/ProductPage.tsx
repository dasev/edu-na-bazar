/**
 * Страница детального товара
 */
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { NumberBox } from 'devextreme-react/number-box'
import { useState } from 'react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { productsApi } from '../../api'
import { useCartStore } from '../../store/cartStore'
import { showToast } from '../../utils/toast'
import ProductReviews from '../../components/ProductReviews/ProductReviews'
import './ProductPage.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ProductPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { addToCart } = useCartStore()
  const [quantity, setQuantity] = useState(1)
  const [adding, setAdding] = useState(false)
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [isImageModalOpen, setIsImageModalOpen] = useState(false)

  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', id],
    queryFn: () => productsApi.getProduct(id!),
    enabled: !!id,
  })

  const handleAddToCart = async () => {
    if (!product) return

    setAdding(true)
    try {
      // Передаем информацию о продукте для гостевой корзины
      await addToCart(product.id, quantity, product)
      showToast.success(`${product.name} добавлен в корзину!`)
    } catch (error) {
      showToast.error('Ошибка добавления в корзину')
    } finally {
      setAdding(false)
    }
  }

  if (isLoading) {
    return (
      <div className="product-page">
        <div className="product-page__container">
          <div className="product-page__breadcrumbs">
            <Skeleton width={300} height={20} />
          </div>
          <div className="product-page__content">
            <div className="product-page__images">
              <Skeleton height={400} />
            </div>
            <div className="product-page__info">
              <Skeleton height={40} width="80%" />
              <Skeleton height={20} width="60%" style={{ marginTop: 12 }} />
              <Skeleton height={60} width="40%" style={{ marginTop: 20 }} />
              <Skeleton height={100} style={{ marginTop: 20 }} />
              <Skeleton height={50} style={{ marginTop: 20 }} />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="product-page">
        <div className="product-page__error">
          <h2>Товар не найден</h2>
          <Button text="Вернуться в каталог" onClick={() => navigate('/catalog')} />
        </div>
      </div>
    )
  }

  const discount = product.old_price
    ? Math.round(((product.old_price - product.price) / product.old_price) * 100)
    : 0

  // Формируем список всех изображений
  // Если есть images - используем только их, иначе берём product.image
  const allImages = product.images && product.images.length > 0
    ? product.images.map((img: any) => img.image_url).filter((url: string) => url)
    : (product.image ? [product.image] : [])

  // Текущее изображение
  const currentImage = selectedImage || allImages[0] || null
  const imageUrl = currentImage
    ? (currentImage.startsWith('http') ? currentImage : `${API_URL}${currentImage}`)
    : 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="500" height="500"%3E%3Crect fill="%23ddd" width="500" height="500"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="24"%3EНет фото%3C/text%3E%3C/svg%3E'

  return (
    <div className="product-page">
      <div className="product-page__container">
        {/* Breadcrumbs */}
        <div className="product-page__breadcrumbs">
          <a href="/">Главная</a>
          <span>/</span>
          <a href="/catalog">Каталог</a>
          <span>/</span>
          <span>{product.name}</span>
        </div>

        <div className="product-page__content">
          {/* Галерея изображений */}
          <div className="product-page__images">
            {allImages.length > 1 && (
              <div className="product-page__thumbnails">
                {allImages.map((img, index) => {
                  const thumbUrl = img.startsWith('http') ? img : `${API_URL}${img}`
                  return (
                    <div
                      key={index}
                      className={`thumbnail ${currentImage === img ? 'active' : ''}`}
                      onClick={() => setSelectedImage(img)}
                    >
                      <img src={thumbUrl} alt={`${product.name} ${index + 1}`} />
                    </div>
                  )
                })}
              </div>
            )}
            <div 
              className="product-page__main-image"
              onClick={() => setIsImageModalOpen(true)}
              style={{ cursor: 'zoom-in' }}
            >
              <img src={imageUrl} alt={product.name} />
            </div>
          </div>

          {/* Модальное окно с увеличенным изображением */}
          {isImageModalOpen && (
            <div 
              className="image-modal"
              onClick={() => setIsImageModalOpen(false)}
            >
              <div className="image-modal__content">
                <button 
                  className="image-modal__close"
                  onClick={() => setIsImageModalOpen(false)}
                >
                  ✕
                </button>
                <img src={imageUrl} alt={product.name} />
              </div>
            </div>
          )}

          {/* Информация */}
          <div className="product-page__info">
            <h1 className="product-page__title">{product.name}</h1>

            {/* Рейтинг */}
            <div className="product-page__rating">
              <span className="rating-stars">⭐ {Number(product.rating).toFixed(1)}</span>
              <span className="rating-reviews">({product.reviews_count} отзывов)</span>
            </div>

            {/* Цена */}
            <div className="product-page__price-block">
              <div className="product-page__price">
                {Number(product.price).toFixed(2)} ₽
                {product.old_price && (
                  <>
                    <span className="product-page__old-price">
                      {Number(product.old_price).toFixed(2)} ₽
                    </span>
                    <span className="product-page__discount">-{discount}%</span>
                  </>
                )}
              </div>
              <div className="product-page__unit">за {product.unit}</div>
            </div>

            {/* Наличие */}
            <div className="product-page__stock">
              {product.in_stock ? (
                <span className="stock-available">✓ В наличии</span>
              ) : (
                <span className="stock-unavailable">✗ Нет в наличии</span>
              )}
            </div>

            {/* Добавление в корзину */}
            {product.in_stock && (
              <div className="product-page__actions">
                <div className="product-page__quantity">
                  <label>Количество:</label>
                  <NumberBox
                    value={quantity}
                    onValueChanged={(e) => setQuantity(e.value || 1)}
                    min={1}
                    max={product.stock_quantity}
                    showSpinButtons={true}
                    width={120}
                  />
                </div>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  <Button
                    text={adding ? 'Добавление...' : 'Добавить в корзину'}
                    type="default"
                    stylingMode="contained"
                    disabled={adding}
                    onClick={handleAddToCart}
                    width={200}
                  />
                  {product.latitude && product.longitude && (
                    <Button
                      icon="map"
                      type="default"
                      stylingMode="contained"
                      hint="Показать на карте"
                      onClick={() => {
                        localStorage.setItem('mapFocusProduct', JSON.stringify({
                          id: product.id,
                          lat: product.latitude,
                          lng: product.longitude
                        }))
                        window.location.href = '/map'
                      }}
                      width={48}
                    />
                  )}
                </div>
              </div>
            )}

            {/* Описание */}
            {product.description && (
              <div className="product-page__description">
                <h3>Описание</h3>
                <p>{product.description}</p>
              </div>
            )}
          </div>
        </div>

        {/* Отзывы и вопросы */}
        <div className="product-page__container">
          <ProductReviews productId={parseInt(id!)} />
        </div>
      </div>
    </div>
  )
}
