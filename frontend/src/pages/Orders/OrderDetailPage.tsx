import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/services/orders'
import './OrderDetailPage.css'

export const OrderDetailPage = () => {
  const { orderId } = useParams<{ orderId: string }>()
  const navigate = useNavigate()

  const { data: order, isLoading, error } = useQuery({
    queryKey: ['order', orderId],
    queryFn: () => ordersApi.getOrder(orderId!),
    enabled: !!orderId
  })

  if (isLoading) {
    return <div className="order-detail-page">Загрузка...</div>
  }

  if (error || !order) {
    return (
      <div className="order-detail-page">
        <div className="error-message">
          <h2>Заказ не найден</h2>
          <p>Заказ #{orderId} не существует или был удален</p>
          <button onClick={() => navigate('/orders')} className="back-button">
            Вернуться к заказам
          </button>
        </div>
      </div>
    )
  }

  const getStatusText = (status: string) => {
    const statusMap: Record<string, string> = {
      'created': 'Создан',
      'paid': 'Подтвержден',
      'processing': 'В обработке',
      'delivering': 'Готов к выдаче',
      'completed': 'Завершен',
      'cancelled': 'Отменен'
    }
    return statusMap[status] || status
  }

  const getStatusClass = (status: string) => {
    return `status-badge status-${status}`
  }

  return (
    <div className="order-detail-page">
      <div className="page-header">
        <button onClick={() => navigate('/orders')} className="back-button">
          ← Назад к заказам
        </button>
        <h1>Заказ #{order.id}</h1>
      </div>

      <div className="order-detail-container">
        {/* Статус и основная информация */}
        <div className="order-info-card">
          <h2>Информация о заказе</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Статус:</span>
              <span className={getStatusClass(order.status)}>
                {getStatusText(order.status)}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Дата создания:</span>
              <span className="info-value">
                {new Date(order.created_at).toLocaleString('ru-RU')}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Способ оплаты:</span>
              <span className="info-value">
                {order.payment_method === 'cash' ? 'Наличные' : 'Карта'}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Адрес доставки:</span>
              <span className="info-value">{order.delivery_address}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Телефон:</span>
              <span className="info-value">{order.delivery_phone}</span>
            </div>
            {order.notes && (
              <div className="info-item full-width">
                <span className="info-label">Комментарий:</span>
                <span className="info-value">{order.notes}</span>
              </div>
            )}
          </div>
        </div>

        {/* Состав заказа */}
        <div className="order-items-card">
          <h2>Состав заказа</h2>
          <div className="items-list">
            {order.items && order.items.length > 0 ? (
              order.items.map((item: any) => (
                <div 
                  key={item.id} 
                  className="order-item"
                  onClick={() => navigate(`/product/${item.product_id}`)}
                  style={{ cursor: 'pointer' }}
                >
                  {item.product_image && (
                    <div className="item-image">
                      <img 
                        src={item.product_image.startsWith('http') 
                          ? item.product_image 
                          : `http://localhost:8000${item.product_image}`
                        } 
                        alt={item.product_name || 'Товар'}
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="80" height="80"%3E%3Crect fill="%23f0f0f0" width="80" height="80"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-size="12"%3EНет фото%3C/text%3E%3C/svg%3E'
                        }}
                      />
                    </div>
                  )}
                  <div className="item-info">
                    <div className="item-name">{item.product_name || `Товар #${item.product_id}`}</div>
                    <div className="item-quantity">
                      {item.quantity} шт × {item.price} ₽
                    </div>
                  </div>
                  <div className="item-total">
                    {(item.quantity * item.price).toFixed(2)} ₽
                  </div>
                </div>
              ))
            ) : (
              <p className="no-items">Нет товаров в заказе</p>
            )}
          </div>

          <div className="order-total">
            <span className="total-label">Итого:</span>
            <span className="total-amount">{order.total_amount} ₽</span>
          </div>
        </div>

        {/* История статусов */}
        <div className="order-timeline-card">
          <h2>История заказа</h2>
          <div className="timeline">
            <div className="timeline-item active">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <div className="timeline-title">Заказ создан</div>
                <div className="timeline-date">
                  {new Date(order.created_at).toLocaleString('ru-RU')}
                </div>
              </div>
            </div>
            {order.status !== 'created' && (
              <div className="timeline-item active">
                <div className="timeline-marker"></div>
                <div className="timeline-content">
                  <div className="timeline-title">{getStatusText(order.status)}</div>
                  <div className="timeline-date">
                    {new Date(order.updated_at).toLocaleString('ru-RU')}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
