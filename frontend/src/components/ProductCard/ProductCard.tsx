import { useNavigate } from 'react-router-dom'
import { Button } from 'devextreme-react/button'
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
    rating: number | string
    reviews_count: number
    category?: string
  }
}

export default function ProductCard({ product }: ProductCardProps) {
  const navigate = useNavigate()
  const { addToCart } = useCartStore()
  
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

  return (
    <div className="product-card" onClick={() => navigate(`/product/${product.id}`)}>
      {/* Изображение */}
      <div className="product-card__image">
        <img src={product.image} alt={product.name} />
        {discount > 0 && (
          <div className="product-card__discount">
            -{discount}%
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
      
      {/* Кнопка */}
      <Button
        text="В корзину"
        type="default"
        width="100%"
        height={44}
        className="product-card__button"
        onClick={handleAddToCart}
      />
    </div>
  )
}
