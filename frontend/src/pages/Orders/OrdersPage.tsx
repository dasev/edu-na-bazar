/**
 * Страница заказов пользователя
 */
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { SelectBox } from 'devextreme-react/select-box';
import { Button } from 'devextreme-react/button';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
import { ordersApi } from '../../api';
import { Order } from '../../api/types';
import { useAuthStore } from '../../store/authStore';
import './OrdersPage.css';

const statusOptions = [
  { value: 'all', label: 'Все заказы' },
  { value: 'created', label: 'Создан' },
  { value: 'paid', label: 'Оплачен' },
  { value: 'processing', label: 'В обработке' },
  { value: 'delivering', label: 'Доставляется' },
  { value: 'completed', label: 'Завершен' },
  { value: 'cancelled', label: 'Отменен' },
];

const statusLabels: Record<string, string> = {
  created: 'Создан',
  paid: 'Оплачен',
  processing: 'В обработке',
  delivering: 'Доставляется',
  completed: 'Завершен',
  cancelled: 'Отменен',
};

const statusColors: Record<string, string> = {
  created: '#3B82F6',
  paid: '#10B981',
  processing: '#F59E0B',
  delivering: '#8B5CF6',
  completed: '#059669',
  cancelled: '#EF4444',
};

export const OrdersPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, token } = useAuthStore();
  const [statusFilter, setStatusFilter] = useState('all');
  const [isReady, setIsReady] = useState(false);

  // Ждем загрузки токена из persist storage
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsReady(true);
      // Редирект если не авторизован после загрузки
      if (!isAuthenticated && !token) {
        navigate('/');
      }
    }, 100);
    return () => clearTimeout(timer);
  }, [isAuthenticated, token, navigate]);

  const { data: ordersData, isLoading, error } = useQuery({
    queryKey: ['orders'],
    queryFn: () => ordersApi.getOrders(),
    enabled: isAuthenticated && isReady, // Запрос только после загрузки токена
  });

  if (!isAuthenticated) {
    return null; // Показываем пустую страницу пока идет редирект
  }

  const orders = ordersData?.data || [];
  
  const filteredOrders = orders.filter((order: Order) => {
    if (statusFilter === 'all') return true;
    return order.status === statusFilter;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="orders-page">
      <div className="orders-container">
        <div className="orders-header">
          <h1>Мои заказы</h1>
          <div className="orders-filter">
            <SelectBox
              items={statusOptions}
              displayExpr="label"
              valueExpr="value"
              value={statusFilter}
              onValueChanged={(e) => setStatusFilter(e.value)}
              placeholder="Фильтр по статусу"
              width={200}
            />
          </div>
        </div>

        {isLoading && (
          <div className="orders-loading">
            {Array.from({ length: 3 }).map((_, index) => (
              <div key={index} className="order-card-skeleton">
                <div className="order-skeleton-header">
                  <Skeleton width={150} height={24} />
                  <Skeleton width={100} height={28} />
                </div>
                <Skeleton width="100%" height={16} />
                <Skeleton width="80%" height={16} style={{ marginTop: 8 }} />
                <div className="order-skeleton-items">
                  <div className="order-skeleton-item">
                    <Skeleton width={60} height={60} />
                    <div style={{ flex: 1 }}>
                      <Skeleton width="70%" height={16} />
                      <Skeleton width="40%" height={14} style={{ marginTop: 4 }} />
                    </div>
                  </div>
                </div>
                <div style={{ marginTop: 16, display: 'flex', justifyContent: 'space-between' }}>
                  <Skeleton width={120} height={20} />
                  <Skeleton width={100} height={36} />
                </div>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="orders-error">
            <div className="error-icon">⚠️</div>
            <h2>Ошибка загрузки</h2>
            <p>Не удалось загрузить список заказов</p>
            <Button
              text="Повторить"
              type="default"
              stylingMode="outlined"
              onClick={() => window.location.reload()}
            />
          </div>
        )}

        {!isLoading && !error && filteredOrders.length === 0 && (
          <div className="orders-empty">
            <div className="empty-icon">📦</div>
            <h2>Заказов пока нет</h2>
            <p>Начните покупки в нашем каталоге</p>
            <Button
              text="В каталог"
              type="default"
              stylingMode="contained"
              onClick={() => navigate('/catalog')}
            />
          </div>
        )}

        {!isLoading && !error && filteredOrders.length > 0 && (
          <div className="orders-list">
            {filteredOrders.map((order: Order) => (
              <div 
                key={order.id} 
                className="order-card"
                onClick={() => navigate(`/orders/${order.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <div className="order-header">
                  <div className="order-info">
                    <div className="order-number">Заказ №{order.id}</div>
                    <div className="order-date">{formatDate(order.created_at)}</div>
                  </div>
                  <div
                    className="order-status"
                    style={{ backgroundColor: statusColors[order.status] }}
                  >
                    {statusLabels[order.status]}
                  </div>
                </div>

                <div className="order-details">
                  <div className="order-detail-item">
                    <span className="detail-label">Адрес доставки:</span>
                    <span className="detail-value">{order.delivery_address}</span>
                  </div>
                  <div className="order-detail-item">
                    <span className="detail-label">Способ оплаты:</span>
                    <span className="detail-value">
                      {order.payment_method === 'card' ? 'Картой' : 'Наличными'}
                    </span>
                  </div>
                </div>

                {order.items && order.items.length > 0 && (
                  <div className="order-items">
                    {order.items.map((item: any) => (
                      <div 
                        key={item.id} 
                        className="order-item"
                        onClick={(e) => {
                          e.stopPropagation() // Предотвращаем переход к деталям заказа
                          navigate(`/product/${item.product_id}`)
                        }}
                      >
                        <div className="order-item-image-wrapper">
                          {item.product_image ? (
                            <img
                              src={item.product_image.startsWith('http') ? item.product_image : `http://localhost:8000${item.product_image}`}
                              alt={item.product_name || 'Товар'}
                              className="order-item-image"
                              onError={(e) => {
                                (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="60" height="60"%3E%3Crect fill="%23f0f0f0" width="60" height="60"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-size="10"%3EНет фото%3C/text%3E%3C/svg%3E'
                              }}
                            />
                          ) : (
                            <div className="order-item-no-image">📦</div>
                          )}
                        </div>
                        <div className="order-item-info">
                          <div className="order-item-name">{item.product_name || `Товар ${item.product_id}`}</div>
                          <div className="order-item-quantity">
                            {item.quantity} шт. × {formatPrice(item.price)}
                          </div>
                        </div>
                        <div className="order-item-total">
                          {formatPrice(item.price * item.quantity)}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <div className="order-footer">
                  <div className="order-total">
                    <span className="total-label">Итого:</span>
                    <span className="total-value">{formatPrice(order.total_amount)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
