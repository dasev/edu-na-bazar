import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { apiClient } from '../../api/client'
import ProductCard from '../../components/ProductCard/ProductCard'
import toast from 'react-hot-toast'
import { useState } from 'react'
import './StoreProductsPage.css'

export default function StoreProductsPage() {
  const { storeId } = useParams<{ storeId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [statusFilter, setStatusFilter] = useState<'active' | 'draft' | 'rejected' | 'moderation'>('active')

  // Получаем товары магазина
  const { data: productsData, isLoading } = useQuery({
    queryKey: ['store-products', storeId, statusFilter],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`, {
        params: { status: statusFilter }
      })
      return response.data
    },
  })

  // Получаем счетчики товаров
  const { data: activeCount = 0 } = useQuery({
    queryKey: ['store-products-count', storeId, 'active'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`, {
        params: { status: 'active', limit: 0 }
      })
      return response.data.meta?.total || 0
    },
  })

  const { data: draftCount = 0 } = useQuery({
    queryKey: ['store-products-count', storeId, 'draft'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`, {
        params: { status: 'draft', limit: 0 }
      })
      return response.data.meta?.total || 0
    },
  })

  const { data: rejectedCount = 0 } = useQuery({
    queryKey: ['store-products-count', storeId, 'rejected'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`, {
        params: { status: 'rejected', limit: 0 }
      })
      return response.data.meta?.total || 0
    },
  })

  const { data: moderationCount = 0 } = useQuery({
    queryKey: ['store-products-count', storeId, 'moderation'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`, {
        params: { status: 'moderation', limit: 0 }
      })
      return response.data.meta?.total || 0
    },
  })

  // Удаление товара (перемещение в корзину)
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/api/my-stores/${storeId}/products/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products'] })
      queryClient.invalidateQueries({ queryKey: ['store-products-count'] })
      toast.success('Товар перемещен в корзину')
    },
    onError: () => {
      toast.error('Ошибка при удалении товара')
    },
  })

  // Отправка на модерацию
  const publishMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.patch(`/api/my-stores/${storeId}/products/${id}/publish`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products'] })
      queryClient.invalidateQueries({ queryKey: ['store-products-count'] })
      toast.success('Товар отправлен на модерацию')
    },
    onError: () => {
      toast.error('Ошибка при отправке товара')
    },
  })

  const products = productsData?.data || []

  const handleDelete = (productId: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот товар?')) {
      deleteMutation.mutate(productId)
    }
  }

  if (isLoading) {
    return <div className="store-products-page">Загрузка...</div>
  }

  return (
    <div className="store-products-page">
      <div className="page-header">
        <Button
          icon="back"
          text="Назад к магазинам"
          onClick={() => navigate('/my-stores')}
          stylingMode="text"
        />
        <h1>Товары магазина</h1>
        <Button
          icon="add"
          text="Добавить товар"
          type="default"
          onClick={() => navigate(`/my-stores/${storeId}/products/new`)}
        />
      </div>

      <div className="products-tabs">
        <button
          className={`tab-button ${statusFilter === 'active' ? 'active' : ''}`}
          onClick={() => setStatusFilter('active')}
        >
          <span className="tab-icon">✓</span>
          <span className="tab-label">Опубликованные</span>
          <span className="tab-count">{activeCount}</span>
        </button>
        <button
          className={`tab-button ${statusFilter === 'moderation' ? 'active' : ''}`}
          onClick={() => setStatusFilter('moderation')}
        >
          <span className="tab-icon">⏳</span>
          <span className="tab-label">На модерации</span>
          <span className="tab-count">{moderationCount}</span>
        </button>
        <button
          className={`tab-button ${statusFilter === 'rejected' ? 'active' : ''}`}
          onClick={() => setStatusFilter('rejected')}
        >
          <span className="tab-icon">❌</span>
          <span className="tab-label">Отклоненные</span>
          <span className="tab-count">{rejectedCount}</span>
        </button>
        <button
          className={`tab-button ${statusFilter === 'draft' ? 'active' : ''}`}
          onClick={() => setStatusFilter('draft')}
        >
          <span className="tab-icon">📦</span>
          <span className="tab-label">Черновики</span>
          <span className="tab-count">{draftCount}</span>
        </button>
      </div>

      {products.length === 0 ? (
        <div className="no-products">
          <p>У вас пока нет товаров</p>
          <Button
            text="Добавить первый товар"
            type="default"
            onClick={() => navigate(`/my-stores/${storeId}/products/new`)}
          />
        </div>
      ) : (
        <div className="products-grid">
          {products.map((product: any) => (
            <div key={product.id} style={{ position: 'relative' }}>
              <ProductCard 
                product={product}
                showManageButtons={false}
              />
              <div className="product-manage-buttons">
                <Button
                  text="Редактировать"
                  icon="edit"
                  type="default"
                  onClick={() => navigate(`/my-stores/${storeId}/products/${product.id}`)}
                  stylingMode="contained"
                />
                {statusFilter === 'draft' || statusFilter === 'rejected' ? (
                  <Button
                    text="На модерацию"
                    icon="upload"
                    type="success"
                    onClick={() => publishMutation.mutate(product.id)}
                    stylingMode="contained"
                  />
                ) : statusFilter === 'moderation' ? (
                  <Button
                    text="Ожидает проверки"
                    icon="clock"
                    type="default"
                    disabled={true}
                    stylingMode="contained"
                  />
                ) : (
                  <Button
                    text="В корзину"
                    icon="trash"
                    type="danger"
                    onClick={() => handleDelete(product.id)}
                    stylingMode="contained"
                  />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
