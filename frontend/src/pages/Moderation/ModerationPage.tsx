import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { apiClient } from '../../api/client'
import ProductCard from '../../components/ProductCard/ProductCard'
import toast from 'react-hot-toast'
import './ModerationPage.css'

export default function ModerationPage() {
  const queryClient = useQueryClient()

  // Получаем товары на модерации
  const { data: productsData, isLoading } = useQuery({
    queryKey: ['moderation-products'],
    queryFn: async () => {
      const response = await apiClient.get('/api/moderation/products')
      return response.data
    },
  })

  // Одобрение товара
  const approveMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.patch(`/api/moderation/products/${id}/approve`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-products'] })
      toast.success('Товар одобрен и опубликован')
    },
    onError: () => {
      toast.error('Ошибка при одобрении товара')
    },
  })

  // Отклонение товара
  const rejectMutation = useMutation({
    mutationFn: async (id: number) => {
      const reason = prompt('Укажите причину отклонения (необязательно):')
      await apiClient.patch(`/api/moderation/products/${id}/reject`, null, {
        params: { reason }
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-products'] })
      toast.success('Товар отклонен')
    },
    onError: () => {
      toast.error('Ошибка при отклонении товара')
    },
  })

  const products = productsData?.data || []
  const total = productsData?.meta?.total || 0

  if (isLoading) {
    return <div className="moderation-page">Загрузка...</div>
  }

  return (
    <div className="moderation-page">
      <div className="page-header">
        <h1>Модерация товаров</h1>
        <div className="moderation-stats">
          <span className="stat-badge">На проверке: {total}</span>
        </div>
      </div>

      {products.length === 0 ? (
        <div className="no-products">
          <p>✅ Нет товаров на модерации</p>
        </div>
      ) : (
        <div className="products-grid">
          {products.map((product: any) => (
            <div key={product.id} style={{ position: 'relative' }}>
              <ProductCard 
                product={product}
                showManageButtons={false}
              />
              <div className="moderation-buttons">
                <Button
                  text="Одобрить"
                  icon="check"
                  type="success"
                  onClick={() => approveMutation.mutate(product.id)}
                  stylingMode="contained"
                />
                <Button
                  text="Отклонить"
                  icon="close"
                  type="danger"
                  onClick={() => rejectMutation.mutate(product.id)}
                  stylingMode="contained"
                />
              </div>
              <div className="product-store-info">
                <span>Магазин ID: {product.store_owner_id}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
