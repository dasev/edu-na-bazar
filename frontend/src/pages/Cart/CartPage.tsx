/**
 * Страница корзины
 */
import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from 'devextreme-react/button'
import { NumberBox } from 'devextreme-react/number-box'
import { useCartStore } from '../../store/cartStore'
import { useAuthStore } from '../../store/authStore'
import { showToast } from '../../utils/toast'
import './CartPage.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const NO_IMAGE = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23ddd" width="100" height="100"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12"%3EНет фото%3C/text%3E%3C/svg%3E'

export default function CartPage() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const { cart, guestCart, isLoading, fetchCart, updateQuantity, removeItem, clearCart } = useCartStore()

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated])

  const handleQuantityChange = async (itemId: string, newQuantity: number) => {
    try {
      await updateQuantity(itemId, newQuantity)
      showToast.success('Количество обновлено')
    } catch (error) {
      showToast.error('Ошибка обновления количества')
    }
  }

  const handleRemoveItem = async (itemId: string) => {
    try {
      await removeItem(itemId)
      showToast.success('Товар удален из корзины')
    } catch (error) {
      showToast.error('Ошибка удаления товара')
    }
  }

  const handleClearCart = async () => {
    try {
      await clearCart()
      showToast.success('Корзина очищена')
    } catch (error) {
      showToast.error('Ошибка очистки корзины')
    }
  }

  if (isLoading) {
    return (
      <div className="cart-page">
        <div className="cart-page__loading">Загрузка корзины...</div>
      </div>
    )
  }

  // Определяем какую корзину показывать
  const items = cart ? cart.items : guestCart.items
  const isEmpty = items.length === 0

  if (isEmpty) {
    return (
      <div className="cart-page">
        <div className="cart-page__empty">
          <div className="empty-icon">🛒</div>
          <h2>Корзина пуста</h2>
          <p>Добавьте товары из каталога</p>
          <Button
            text="Перейти в каталог"
            type="default"
            stylingMode="contained"
            onClick={() => navigate('/catalog')}
          />
        </div>
      </div>
    )
  }

  // Вычисляем итого для гостевой корзины
  const total = cart 
    ? cart.total 
    : guestCart.items.reduce((sum, item) => sum + (Number(item.product?.price) || 0) * item.quantity, 0)
  
  const itemsCount = cart 
    ? cart.items_count 
    : guestCart.items.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <div className="cart-page">
      <div className="cart-page__container">
        <div className="cart-page__header">
          <h1>Корзина</h1>
          <Button
            text="Очистить корзину"
            stylingMode="text"
            onClick={handleClearCart}
          />
        </div>

        <div className="cart-page__content">
          {/* Список товаров */}
          <div className="cart-page__items">
            {items.map((item: any) => {
              // Для серверной корзины
              if (cart) {
                return (
                  <div key={item.id} className="cart-item">
                    <div className="cart-item__image" onClick={() => navigate(`/product/${item.product_id}`)} style={{ cursor: 'pointer' }}>
                      <img
                        src={item.product_image ? (item.product_image.startsWith('http') ? item.product_image : `${API_URL}${item.product_image}`) : NO_IMAGE}
                        alt={item.product_name}
                      />
                    </div>

                    <div className="cart-item__info">
                      <h3 className="cart-item__name" onClick={() => navigate(`/product/${item.product_id}`)} style={{ cursor: 'pointer' }}>{item.product_name}</h3>
                      <div className="cart-item__price">
                        {Number(item.product_price).toFixed(2)} ₽
                      </div>
                      {!item.product_in_stock && (
                        <div className="cart-item__out-of-stock">
                          Нет в наличии
                        </div>
                      )}
                    </div>

                    <div className="cart-item__quantity">
                      <NumberBox
                        value={item.quantity}
                        onValueChanged={(e) => handleQuantityChange(item.id, e.value || 1)}
                        min={1}
                        max={99}
                        showSpinButtons={true}
                        width={120}
                        disabled={!item.product_in_stock}
                      />
                    </div>

                    <div className="cart-item__subtotal">
                      {Number(item.subtotal).toFixed(2)} ₽
                    </div>

                    <div className="cart-item__actions">
                      <Button
                        icon="trash"
                        stylingMode="text"
                        onClick={() => handleRemoveItem(item.id)}
                      />
                    </div>
                  </div>
                )
              }
              
              // Для гостевой корзины
              return (
                <div key={item.product_id} className="cart-item">
                  <div className="cart-item__image" onClick={() => navigate(`/product/${item.product_id}`)} style={{ cursor: 'pointer' }}>
                    <img
                      src={item.product?.image ? (item.product.image.startsWith('http') ? item.product.image : `${API_URL}${item.product.image}`) : NO_IMAGE}
                      alt={item.product?.name || 'Товар'}
                    />
                  </div>

                  <div className="cart-item__info">
                    <h3 className="cart-item__name" onClick={() => navigate(`/product/${item.product_id}`)} style={{ cursor: 'pointer' }}>{item.product?.name || 'Товар'}</h3>
                    <div className="cart-item__price">
                      {Number(item.product?.price || 0).toFixed(2)} ₽
                    </div>
                  </div>

                  <div className="cart-item__quantity">
                    <NumberBox
                      value={item.quantity}
                      onValueChanged={(e) => handleQuantityChange(item.product_id, e.value || 1)}
                      min={1}
                      max={99}
                      showSpinButtons={true}
                      width={120}
                    />
                  </div>

                  <div className="cart-item__subtotal">
                    {(Number(item.product?.price || 0) * item.quantity).toFixed(2)} ₽
                  </div>

                  <div className="cart-item__actions">
                    <Button
                      icon="trash"
                      stylingMode="text"
                      onClick={() => handleRemoveItem(item.product_id)}
                    />
                  </div>
                </div>
              )
            })}
          </div>

          {/* Итого */}
          <div className="cart-page__summary">
            <div className="cart-summary">
              <h3>Итого</h3>
              
              <div className="cart-summary__row">
                <span>Товаров:</span>
                <span>{itemsCount} шт</span>
              </div>

              <div className="cart-summary__row cart-summary__total">
                <span>Сумма:</span>
                <span>{Number(total).toFixed(2)} ₽</span>
              </div>

              {!isAuthenticated && (
                <div className="cart-summary__auth-hint">
                  <p>💡 Войдите, чтобы оформить заказ</p>
                </div>
              )}

              <Button
                text={isAuthenticated ? "Оформить заказ" : "Войти и оформить"}
                type="default"
                stylingMode="contained"
                width="100%"
                onClick={() => navigate(isAuthenticated ? '/checkout' : '/')}
              />

              <Link to="/catalog" className="cart-summary__continue">
                Продолжить покупки
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
