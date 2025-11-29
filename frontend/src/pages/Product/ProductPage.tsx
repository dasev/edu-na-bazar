/**
 * Страница детального товара
 */
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { NumberBox } from 'devextreme-react/number-box'
import { useState, useEffect, useRef } from 'react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { productsApi } from '../../api'
import { useCartStore } from '../../store/cartStore'
import { showToast } from '../../utils/toast'
import ProductReviews from '../../components/ProductReviews/ProductReviews'
import './ProductPage.css'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
mapboxgl.accessToken = 'pk.eyJ1Ijoic2VyZ2VqZGFuNDUyIiwiYSI6ImNtaTd0dzQ4ajA0bHkyanIyNWJwa2JrNXYifQ.AWJBOIEEXVb-6AIKrbRXmw'

export default function ProductPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { addToCart } = useCartStore()
  const [quantity, setQuantity] = useState(1)
  const [adding, setAdding] = useState(false)
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [isImageModalOpen, setIsImageModalOpen] = useState(false)
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)

  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', id],
    queryFn: () => productsApi.getProduct(id!),
    enabled: !!id,
  })

  // Запрос данных о магазине через API клиент
  const { data: storeOwner } = useQuery({
    queryKey: ['store-owner', product?.store_owner_id],
    queryFn: async () => {
      if (!product?.store_owner_id) return null
      const response = await fetch(`${API_URL}/api/store-owners/${product.store_owner_id}`)
      if (!response.ok) throw new Error('Failed to fetch store owner')
      return response.json()
    },
    enabled: !!product?.store_owner_id,
  })

  // Инициализация мини-карты
  useEffect(() => {
    if (!product?.latitude || !product?.longitude || !mapContainer.current || map.current) return

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        glyphs: 'mapbox://fonts/mapbox/{fontstack}/{range}.pbf',
        sources: {
          'google-tiles': {
            type: 'raster',
            tiles: [
              'https://mt0.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
              'https://mt1.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
              'https://mt2.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
              'https://mt3.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}'
            ],
            tileSize: 256,
            attribution: ''
          }
        },
        layers: [
          {
            id: 'google-tiles-layer',
            type: 'raster',
            source: 'google-tiles',
            minzoom: 0,
            maxzoom: 22
          }
        ]
      },
      center: [product.longitude, product.latitude],
      zoom: 13,
      interactive: true, // Включаем взаимодействие (скролл, зум, перемещение)
      attributionControl: false, // Убираем водяные знаки Mapbox
      logoPosition: 'bottom-right' // Позиция логотипа (если нужно)
    })
    
    // Убираем логотип Mapbox
    const mapboxLogo = mapContainer.current.querySelector('.mapboxgl-ctrl-logo')
    if (mapboxLogo) {
      (mapboxLogo as HTMLElement).style.display = 'none'
    }

    // Добавляем маркер
    new mapboxgl.Marker({ color: '#667eea' })
      .setLngLat([product.longitude, product.latitude])
      .addTo(map.current)

    return () => {
      map.current?.remove()
      map.current = null
    }
  }, [product?.latitude, product?.longitude])

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

        {/* Информация о продавце и местоположении */}
        <div className="product-page__seller-section">
          <div className="product-page__seller-info">
            <h3>🏪 Продавец</h3>
            {storeOwner ? (
              <div className="seller-card">
                <div className="seller-card__header">
                  {storeOwner.logo && (
                    <img 
                      src={storeOwner.logo.startsWith('http') ? storeOwner.logo : `${API_URL}${storeOwner.logo}`} 
                      alt={storeOwner.name}
                      className="seller-card__logo"
                    />
                  )}
                  <div className="seller-card__info">
                    <h4>{storeOwner.name}</h4>
                    {storeOwner.legal_name && (
                      <p className="seller-card__legal-name">{storeOwner.legal_name}</p>
                    )}
                    {storeOwner.inn && (
                      <p className="seller-card__inn">ИНН: {storeOwner.inn}</p>
                    )}
                  </div>
                </div>
                
                {storeOwner.description && (
                  <p className="seller-card__description">{storeOwner.description}</p>
                )}
                
                <div className="seller-card__contacts">
                  {storeOwner.phone && (
                    <div className="contact-item">
                      <span className="contact-icon">📞</span>
                      <a href={`tel:${storeOwner.phone}`}>{storeOwner.phone}</a>
                    </div>
                  )}
                  {storeOwner.email && (
                    <div className="contact-item">
                      <span className="contact-icon">✉️</span>
                      <a href={`mailto:${storeOwner.email}`}>{storeOwner.email}</a>
                    </div>
                  )}
                  {storeOwner.address && (
                    <div className="contact-item">
                      <span className="contact-icon">📍</span>
                      <span>{storeOwner.address}</span>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <Skeleton height={200} />
            )}
          </div>

          {/* Местоположение товара */}
          {(product.location || (product.latitude && product.longitude)) && (
            <div className="product-page__location">
              <h3>📍 Местоположение товара</h3>
              
              {product.location && (
                <div className="location-address">
                  <p>{product.location}</p>
                </div>
              )}

              {product.latitude && product.longitude && (
                <div className="location-map-container">
                  <div 
                    ref={mapContainer} 
                    className="location-mini-map"
                    style={{ borderRadius: '12px', overflow: 'hidden' }}
                  />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Отзывы и вопросы */}
        <div className="product-page__container">
          <ProductReviews productId={parseInt(id!)} />
        </div>
      </div>
    </div>
  )
}
