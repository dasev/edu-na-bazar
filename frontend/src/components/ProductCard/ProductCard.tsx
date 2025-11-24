import { useNavigate } from 'react-router-dom'
import { Button } from 'devextreme-react/button'
import { useState } from 'react'
import { useCartStore } from '../../store/cartStore'
import { showToast } from '../../utils/toast'
import './ProductCard.css'

interface ProductCardProps {
  product: {
    id: string
    name: string
    price: number | string
    old_price?: number | string
    image: string
    images?: Array<{ image_url: string }>
    rating: number | string
    reviews_count: number
    category?: string
    latitude?: number
    longitude?: number
  }
}

export default function ProductCard({ product }: ProductCardProps) {
  const navigate = useNavigate()
  const { addToCart } = useCartStore()
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
  // Формируем список всех изображений
  const allImages = product.images && product.images.length > 0
    ? product.images.map(img => img.image_url)
    : (product.image ? [product.image] : [])
  
  // Текущее изображение
  const currentImageUrl = allImages[currentImageIndex] || product.image
  const imageUrl = currentImageUrl
    ? (currentImageUrl.startsWith('http') ? currentImageUrl : `${API_URL}${currentImageUrl}`)
    : 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="300"%3E%3Crect fill="%23ddd" width="300" height="300"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="18"%3EНет фото%3C/text%3E%3C/svg%3E'
  
  const discount = product.old_price 
    ? Math.round((1 - Number(product.price) / Number(product.old_price)) * 100)
    : 0

  const handleAddToCart = async (e: any) => {
    e.event?.stopPropagation()
    try {
      // Передаем информацию о продукте для гостевой корзины
      await addToCart(product.id, 1, product)
      showToast.success(`${product.name} добавлен в корзину!`)
    } catch (error) {
      showToast.error('Ошибка добавления в корзину')
      console.error('Error adding to cart:', error)
    }
  }

  // Обработка движения мыши для переключения изображений
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (allImages.length <= 1) return
    
    const card = e.currentTarget
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const cardWidth = rect.width
    
    // Делим карточку на зоны по количеству изображений
    const zoneWidth = cardWidth / allImages.length
    const newIndex = Math.min(Math.floor(x / zoneWidth), allImages.length - 1)
    
    setCurrentImageIndex(newIndex)
  }

  const handleMouseLeave = () => {
    setCurrentImageIndex(0)
  }

  return (
    <div className="product-card" onClick={() => navigate(`/product/${product.id}`)}>
      {/* Изображение */}
      <div 
        className="product-card__image"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        <img 
          src={imageUrl} 
          alt={product.name}
        />
        {discount > 0 && (
          <div className="product-card__discount">
            -{discount}%
          </div>
        )}
        {/* Индикаторы изображений */}
        {allImages.length > 1 && (
          <div className="product-card__image-indicators">
            {allImages.map((_, index) => (
              <div
                key={index}
                className={`indicator ${index === currentImageIndex ? 'active' : ''}`}
              />
            ))}
          </div>
        )}
      </div>
      
      {/* Цена */}
      <div className="product-card__price">
        <span className="current">{Number(product.price).toLocaleString()} ₽</span>
        {product.old_price && (
          <span className="old">{Number(product.old_price).toLocaleString()} ₽</span>
        )}
      </div>
      
      {/* Название */}
      <div className="product-card__name">
        {product.name}
      </div>
      
      {/* Рейтинг */}
      <div className="product-card__rating">
        <span className="stars">★ {Number(product.rating).toFixed(1)}</span>
        <span className="reviews">({product.reviews_count})</span>
      </div>
      
      {/* Кнопки */}
      <div style={{ display: 'flex', gap: '8px', width: '100%' }}>
        <Button
          text="В корзину"
          type="default"
          height={44}
          className="product-card__button"
          onClick={handleAddToCart}
          style={{ flex: 1 }}
        />
        {product.latitude && product.longitude && (
          <Button
            icon="map"
            type="default"
            height={44}
            hint="Показать на карте"
            onClick={() => {
              // Сохраняем ID товара и координаты в localStorage
              localStorage.setItem('mapFocusProduct', JSON.stringify({
                id: product.id,
                lat: product.latitude,
                lng: product.longitude
              }))
              // Переходим на карту
              window.location.href = '/map'
            }}
            style={{ width: '44px', minWidth: '44px' }}
          />
        )}
      </div>
    </div>
  )
}
