import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { TextBox } from 'devextreme-react/text-box'
import { apiClient } from '../../api/client'
import './StoresPage.css'

export default function StoresPage() {
  const navigate = useNavigate()

  // Получаем все магазины
  const { data: stores = [], isLoading } = useQuery({
    queryKey: ['stores'],
    queryFn: async () => {
      const response = await apiClient.get('/api/stores')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="stores-page">Загрузка...</div>
  }

  return (
    <div className="stores-page">
      <div className="page-header">
        <h1>Магазины</h1>
        <p className="page-subtitle">Фермерские хозяйства и магазины на платформе</p>
      </div>

      <div className="stores-filter">
        <TextBox
          placeholder="Поиск магазинов..."
          mode="search"
          width={400}
        />
      </div>

      {stores.length === 0 ? (
        <div className="no-stores">
          <p>Магазины не найдены</p>
        </div>
      ) : (
        <div className="stores-grid">
          {stores.map((store: any) => (
            <div key={store.id} className="store-card">
              <div className="store-banner">
                {store.banner ? (
                  <img src={store.banner} alt={store.name} />
                ) : (
                  <div className="no-banner">🏪</div>
                )}
                {store.logo && (
                  <div className="store-logo">
                    <img src={store.logo} alt={store.name} />
                  </div>
                )}
              </div>
              <div className="store-info">
                <h3>{store.name}</h3>
                <p className="store-description">{store.description}</p>
                <div className="store-meta">
                  <span>📍 {store.address}</span>
                  {store.phone && <span>📞 {store.phone}</span>}
                </div>
                <div className="store-status">
                  <span className={`status-badge status-${store.status}`}>
                    {store.status === 'approved' ? '✅ Активен' : 
                     store.status === 'pending' ? '⏳ На модерации' : 
                     '❌ Отклонен'}
                  </span>
                </div>
              </div>
              <div className="store-actions">
                <button
                  className="btn-catalog"
                  onClick={() => navigate(`/catalog?store_id=${store.id}`)}
                >
                  Перейти в каталог
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
