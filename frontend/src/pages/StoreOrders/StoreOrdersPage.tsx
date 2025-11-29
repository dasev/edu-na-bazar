/**
 * Страница заказов магазина
 */
import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { SelectBox } from 'devextreme-react/select-box'
import { storeOrdersApi } from '../../api/services/storeOrders'
import { showToast } from '../../utils/toast'
import type { Order } from '../../api/types'
import './StoreOrdersPage.css'

const statusOptions = [
  { id: 'all', name: 'Все заказы' },
  { id: 'created', name: 'Новые' },
  { id: 'paid', name: 'Оплачены' },
  { id: 'processing', name: 'В обработке' },
  { id: 'delivering', name: 'Доставляются' },
  { id: 'completed', name: 'Завершены' },
  { id: 'cancelled', name: 'Отменены' },
]

const statusLabels: Record<string, string> = {
  created: 'Новый',
  paid: 'Оплачен',
  processing: 'В обработке',
  delivering: 'Доставляется',
  completed: 'Завершен',
  cancelled: 'Отменен',
}

const statusColors: Record<string, string> = {
  created: '#4CAF50',
  paid: '#2196F3',
  processing: '#FF9800',
  delivering: '#9C27B0',
  completed: '#607D8B',
  cancelled: '#F44336',
}

export default function StoreOrdersPage() {
  const { storeId } = useParams<{ storeId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [statusFilter, setStatusFilter] = useState('all')
  const [updatingOrderId, setUpdatingOrderId] = useState<number | null>(null)

  // Загрузка заказов
  const { data, isLoading, error } = useQuery({
    queryKey: ['store-orders', storeId, statusFilter],
    queryFn: () => storeOrdersApi.getStoreOrders(
      parseInt(storeId!),
      { status: statusFilter === 'all' ? undefined : statusFilter }
    ),
    enabled: !!storeId,
    refetchOnWindowFocus: false,
    staleTime: 30000, // 30 секунд
  })

  // Обновление статуса заказа
  const updateStatusMutation = useMutation({
    mutationFn: ({ orderId, status }: { orderId: number; status: string }) =>
      storeOrdersApi.updateOrderStatus(parseInt(storeId!), orderId, status),
    onMutate: async ({ orderId, status }) => {
      setUpdatingOrderId(orderId)
      
      // Отменяем текущие запросы
      await queryClient.cancelQueries({ 
        queryKey: ['store-orders', storeId, statusFilter] 
      })
      
      // Сохраняем предыдущее состояние
      const previousOrders = queryClient.getQueryData(['store-orders', storeId, statusFilter])
      
      // Оптимистично обновляем UI
      queryClient.setQueryData(['store-orders', storeId, statusFilter], (old: any) => {
        if (!old) return old
        return {
          ...old,
          data: old.data.map((order: Order) =>
            order.id === orderId ? { ...order, status } : order
          )
        }
      })
      
      return { previousOrders }
    },
    onSuccess: () => {
      showToast.success('Статус заказа обновлен')
      setUpdatingOrderId(null)
    },
    onError: (error: any, variables, context: any) => {
      // Откатываем изменения при ошибке
      if (context?.previousOrders) {
        queryClient.setQueryData(
          ['store-orders', storeId, statusFilter],
          context.previousOrders
        )
      }
      showToast.error(error.response?.data?.detail || 'Ошибка обновления статуса')
      setUpdatingOrderId(null)
    },
    onSettled: () => {
      // Обновляем данные после завершения
      queryClient.invalidateQueries({ 
        queryKey: ['store-orders', storeId, statusFilter],
        exact: true 
      })
    },
  })

  const handleStatusChange = (orderId: number, newStatus: string, currentStatus: string) => {
    // Предотвращаем повторный вызов если уже обновляется или статус не изменился
    if (updatingOrderId === orderId || newStatus === currentStatus) return
    updateStatusMutation.mutate({ orderId, status: newStatus })
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const formatPrice = (price: number) => {
    return `${price.toFixed(2)} ₽`
  }

  if (isLoading) {
    return (
      <div className="store-orders-page">
        <div className="loading">Загрузка заказов...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="store-orders-page">
        <div className="error">Ошибка загрузки заказов</div>
      </div>
    )
  }

  const orders = data?.data || []

  return (
    <div className="store-orders-page">
      <div className="page-header">
        <Button
          icon="back"
          text="Назад"
          onClick={() => navigate('/my-stores')}
          stylingMode="text"
        />
        <h1>Заказы магазина</h1>
      </div>

      <div className="filters">
        <SelectBox
          dataSource={statusOptions}
          value={statusFilter}
          onValueChanged={(e) => setStatusFilter(e.value)}
          displayExpr="name"
          valueExpr="id"
          width={250}
        />
        <div className="orders-count">
          Найдено заказов: {data?.meta.total || 0}
        </div>
      </div>

      {orders.length === 0 ? (
        <div className="no-orders">
          <p>Заказов не найдено</p>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order: Order) => (
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
                  className="order-status-badge"
                  style={{ backgroundColor: statusColors[order.status] }}
                >
                  {statusLabels[order.status]}
                </div>
              </div>

              <div className="order-details">
                <div className="detail-row">
                  <span className="detail-label">Адрес доставки:</span>
                  <span className="detail-value">{order.delivery_address}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Телефон:</span>
                  <span className="detail-value">{order.delivery_phone}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Оплата:</span>
                  <span className="detail-value">
                    {order.payment_method === 'card' ? 'Картой' : 'Наличными'}
                  </span>
                </div>
                {order.notes && (
                  <div className="detail-row">
                    <span className="detail-label">Комментарий:</span>
                    <span className="detail-value">{order.notes}</span>
                  </div>
                )}
              </div>

              {order.items && order.items.length > 0 && (
                <div className="order-items">
                  <h4>Товары:</h4>
                  {order.items.map((item) => (
                    <div 
                      key={item.id} 
                      className="order-item"
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate(`/product/${item.product_id}`)
                      }}
                      style={{ cursor: 'pointer' }}
                    >
                      {item.product_image && (
                        <img 
                          src={item.product_image.startsWith('http') ? item.product_image : `http://localhost:8000${item.product_image}`}
                          alt={item.product_name || 'Товар'}
                          className="item-image"
                        />
                      )}
                      <div className="item-info">
                        <span className="item-name">{item.product_name || `Товар ${item.product_id}`}</span>
                        <span className="item-quantity">× {item.quantity}</span>
                      </div>
                      <div className="item-price">
                        {formatPrice(item.subtotal)}
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
                <div className="order-actions">
                  <SelectBox
                    dataSource={statusOptions.filter(s => s.id !== 'all')}
                    value={order.status}
                    onValueChanged={(e) => handleStatusChange(order.id, e.value, order.status)}
                    displayExpr="name"
                    valueExpr="id"
                    width={200}
                    placeholder="Изменить статус"
                    disabled={updatingOrderId === order.id}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
