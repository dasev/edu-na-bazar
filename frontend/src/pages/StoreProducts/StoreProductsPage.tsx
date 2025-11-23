import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { TextBox } from 'devextreme-react/text-box'
import { SelectBox } from 'devextreme-react/select-box'
import { apiClient } from '../../api/client'
import toast from 'react-hot-toast'
import './StoreProductsPage.css'

export default function StoreProductsPage() {
  const { storeId } = useParams<{ storeId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  // Получаем товары магазина
  const { data: productsData, isLoading } = useQuery({
    queryKey: ['store-products', storeId],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`)
      return response.data
    },
  })

  // Получаем категории для фильтра
  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await apiClient.get('/api/categories/')
      return response.data
    },
  })

  // Удаление товара
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/api/my-stores/${storeId}/products/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
      toast.success('Товар удален')
    },
    onError: () => {
      toast.error('Ошибка при удалении товара')
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

      <div className="products-filter">
        <TextBox
          placeholder="Поиск товаров..."
          mode="search"
          width={300}
        />
        <SelectBox
          placeholder="Все категории"
          dataSource={categories}
          displayExpr="name"
          valueExpr="id"
          width={200}
        />
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
            <div key={product.id} className="product-card">
              <div className="product-image">
                {product.image ? (
                  <img src={product.image} alt={product.name} />
                ) : (
                  <div className="no-image">📦</div>
                )}
                {!product.in_stock && (
                  <div className="out-of-stock-badge">Нет в наличии</div>
                )}
              </div>
              <div className="product-info">
                <h3>{product.name}</h3>
                <p className="product-description">{product.description}</p>
                <div className="product-meta">
                  <span className="product-price">{product.price} ₽/{product.unit}</span>
                  <span className="product-rating">⭐ {product.rating}</span>
                </div>
              </div>
              <div className="product-actions">
                <Button
                  text="Редактировать"
                  icon="edit"
                  onClick={() => navigate(`/my-stores/${storeId}/products/${product.id}`)}
                  stylingMode="outlined"
                />
                <Button
                  text="Удалить"
                  icon="trash"
                  onClick={() => handleDelete(product.id)}
                  stylingMode="outlined"
                  type="danger"
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
