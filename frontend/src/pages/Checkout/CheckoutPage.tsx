/**
 * Страница оформления заказа
 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from 'devextreme-react/button'
import { TextBox } from 'devextreme-react/text-box'
import { TextArea } from 'devextreme-react/text-area'
import { SelectBox } from 'devextreme-react/select-box'
import { DateBox } from 'devextreme-react/date-box'
import { useCartStore } from '../../store/cartStore'
import { useAuthStore } from '../../store/authStore'
import { ordersApi } from '../../api'
import { showToast } from '../../utils/toast'
import type { OrderCreate } from '../../api/types'
import './CheckoutPage.css'

const paymentMethods = [
  { id: 'card', name: 'Банковская карта' },
  { id: 'cash', name: 'Наличные при получении' },
  { id: 'online', name: 'Онлайн оплата' },
]

export default function CheckoutPage() {
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuthStore()
  const { cart, fetchCart, clearCart } = useCartStore()
  
  const [formData, setFormData] = useState({
    contact_name: user?.full_name || '',
    contact_phone: user?.phone || '',
    delivery_address: '',
    delivery_time: null as Date | null,
    delivery_comment: '',
    payment_method: 'card',
    comment: '',
  })
  
  const [submitting, setSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/')
      return
    }
    if (!cart || cart.items.length === 0) {
      navigate('/cart')
      return
    }
    fetchCart()
  }, [isAuthenticated, cart, fetchCart, navigate])

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.contact_name.trim()) {
      newErrors.contact_name = 'Введите ФИО'
    }
    if (!formData.contact_phone.trim()) {
      newErrors.contact_phone = 'Введите телефон'
    }
    if (!formData.delivery_address.trim()) {
      newErrors.delivery_address = 'Введите адрес доставки'
    }
    if (!formData.payment_method) {
      newErrors.payment_method = 'Выберите способ оплаты'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!validate() || !cart) return

    setSubmitting(true)
    try {
      const orderData: OrderCreate = {
        items: cart.items.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
        })),
        delivery_address: formData.delivery_address,
        delivery_time: formData.delivery_time?.toISOString(),
        delivery_comment: formData.delivery_comment || undefined,
        payment_method: formData.payment_method,
        contact_phone: formData.contact_phone,
        contact_name: formData.contact_name,
        comment: formData.comment || undefined,
      }

      const order = await ordersApi.createOrder(orderData)
      
      // Очищаем корзину
      await clearCart()
      
      // Показываем успех и переходим
      showToast.success(`Заказ №${order.id.slice(0, 8)} успешно создан!`)
      setTimeout(() => navigate('/orders'), 1500)
    } catch (error: any) {
      showToast.error(error.response?.data?.detail || 'Ошибка создания заказа')
    } finally {
      setSubmitting(false)
    }
  }

  if (!cart || cart.items.length === 0) {
    return null
  }

  return (
    <div className="checkout-page">
      <div className="checkout-page__container">
        <h1>Оформление заказа</h1>

        <div className="checkout-page__content">
          {/* Форма */}
          <div className="checkout-page__form">
            <div className="checkout-section">
              <h2>Контактные данные</h2>
              
              <div className="form-field">
                <label>ФИО *</label>
                <TextBox
                  value={formData.contact_name}
                  onValueChanged={(e) => setFormData({ ...formData, contact_name: e.value })}
                  placeholder="Иван Иванов"
                  isValid={!errors.contact_name}
                  validationError={errors.contact_name}
                />
              </div>

              <div className="form-field">
                <label>Телефон *</label>
                <TextBox
                  value={formData.contact_phone}
                  onValueChanged={(e) => setFormData({ ...formData, contact_phone: e.value })}
                  placeholder="+7 (999) 123-45-67"
                  mask="+7 (000) 000-00-00"
                  isValid={!errors.contact_phone}
                  validationError={errors.contact_phone}
                />
              </div>
            </div>

            <div className="checkout-section">
              <h2>Доставка</h2>
              
              <div className="form-field">
                <label>Адрес доставки *</label>
                <TextArea
                  value={formData.delivery_address}
                  onValueChanged={(e) => setFormData({ ...formData, delivery_address: e.value })}
                  placeholder="г. Москва, ул. Ленина, д. 10, кв. 5"
                  height={80}
                  isValid={!errors.delivery_address}
                  validationError={errors.delivery_address}
                />
              </div>

              <div className="form-field">
                <label>Желаемое время доставки</label>
                <DateBox
                  value={formData.delivery_time}
                  onValueChanged={(e) => setFormData({ ...formData, delivery_time: e.value })}
                  type="datetime"
                  min={new Date()}
                  placeholder="Выберите дату и время"
                />
              </div>

              <div className="form-field">
                <label>Комментарий к доставке</label>
                <TextArea
                  value={formData.delivery_comment}
                  onValueChanged={(e) => setFormData({ ...formData, delivery_comment: e.value })}
                  placeholder="Домофон не работает, позвоните заранее"
                  height={60}
                />
              </div>
            </div>

            <div className="checkout-section">
              <h2>Оплата</h2>
              
              <div className="form-field">
                <label>Способ оплаты *</label>
                <SelectBox
                  items={paymentMethods}
                  value={formData.payment_method}
                  onValueChanged={(e) => setFormData({ ...formData, payment_method: e.value })}
                  displayExpr="name"
                  valueExpr="id"
                  isValid={!errors.payment_method}
                  validationError={errors.payment_method}
                />
              </div>

              <div className="form-field">
                <label>Комментарий к заказу</label>
                <TextArea
                  value={formData.comment}
                  onValueChanged={(e) => setFormData({ ...formData, comment: e.value })}
                  placeholder="Дополнительные пожелания"
                  height={60}
                />
              </div>
            </div>
          </div>

          {/* Сводка заказа */}
          <div className="checkout-page__summary">
            <div className="order-summary">
              <h3>Ваш заказ</h3>

              <div className="order-summary__items">
                {cart.items.map((item) => (
                  <div key={item.id} className="order-summary__item">
                    <span className="item-name">
                      {item.product_name} × {item.quantity}
                    </span>
                    <span className="item-price">
                      {item.subtotal.toFixed(2)} ₽
                    </span>
                  </div>
                ))}
              </div>

              <div className="order-summary__total">
                <span>Итого:</span>
                <span>{cart.total.toFixed(2)} ₽</span>
              </div>

              <Button
                text={submitting ? 'Оформление...' : 'Оформить заказ'}
                type="default"
                stylingMode="contained"
                width="100%"
                disabled={submitting}
                onClick={handleSubmit}
              />

              <div className="order-summary__note">
                Нажимая кнопку, вы соглашаетесь с условиями доставки и оплаты
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
