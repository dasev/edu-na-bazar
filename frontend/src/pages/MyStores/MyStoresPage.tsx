/**
 * Страница "Мои магазины"
 */
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Button } from 'devextreme-react/button';
import { myStoresApi, Store } from '../../api/services/myStores';
import { useAuthStore } from '../../store/authStore';
import './MyStoresPage.css';

export const MyStoresPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();

  // Автоматический редирект если не авторизован
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const { data: stores, isLoading, error, refetch } = useQuery({
    queryKey: ['my-stores'],
    queryFn: () => myStoresApi.getMyStores(),
    enabled: isAuthenticated,
  });

  if (!isAuthenticated) {
    return null;
  }

  const getStatusBadge = (status: string) => {
    const badges = {
      pending: { text: 'На модерации', className: 'status-pending' },
      active: { text: 'Активен', className: 'status-active' },
      suspended: { text: 'Приостановлен', className: 'status-suspended' },
      rejected: { text: 'Отклонен', className: 'status-rejected' },
    };
    const badge = badges[status as keyof typeof badges] || badges.pending;
    return <span className={`store-status ${badge.className}`}>{badge.text}</span>;
  };

  return (
    <div className="my-stores-page">
      <div className="my-stores-container">
        <div className="my-stores-header">
          <h1>Мои магазины</h1>
          <Button
            text="Создать магазин"
            type="default"
            stylingMode="contained"
            icon="plus"
            onClick={() => navigate('/my-stores/create')}
          />
        </div>

        {isLoading && (
          <div className="stores-loading">
            <div className="loading-spinner">Загрузка...</div>
          </div>
        )}

        {error && (
          <div className="stores-error">
            <p>Ошибка загрузки магазинов</p>
            <Button text="Повторить" onClick={() => refetch()} />
          </div>
        )}

        {!isLoading && !error && stores && stores.length === 0 && (
          <div className="stores-empty">
            <div className="empty-icon">🏪</div>
            <h2>У вас пока нет магазинов</h2>
            <p>Создайте свой первый магазин и начните продавать товары</p>
            <Button
              text="Создать магазин"
              type="default"
              stylingMode="contained"
              onClick={() => navigate('/my-stores/create')}
            />
          </div>
        )}

        {!isLoading && !error && stores && stores.length > 0 && (
          <div className="stores-grid">
            {stores.map((store: Store) => (
              <div key={store.id} className="store-card">
                <div className="store-card__header">
                  {store.logo ? (
                    <img src={store.logo} alt={store.name} className="store-logo" />
                  ) : (
                    <div className="store-logo-placeholder">🏪</div>
                  )}
                  <div className="store-info">
                    <h3>{store.name}</h3>
                    <p className="store-legal-name">{store.legal_name}</p>
                    {getStatusBadge(store.status)}
                  </div>
                </div>

                <div className="store-card__body">
                  <div className="store-detail">
                    <span className="detail-label">ИНН:</span>
                    <span className="detail-value">{store.inn}</span>
                  </div>
                  {store.kpp && (
                    <div className="store-detail">
                      <span className="detail-label">КПП:</span>
                      <span className="detail-value">{store.kpp}</span>
                    </div>
                  )}
                  <div className="store-detail">
                    <span className="detail-label">Адрес:</span>
                    <span className="detail-value">{store.address}</span>
                  </div>
                  {store.phone && (
                    <div className="store-detail">
                      <span className="detail-label">Телефон:</span>
                      <span className="detail-value">{store.phone}</span>
                    </div>
                  )}
                </div>

                <div className="store-card__footer">
                  <Button
                    text="Товары"
                    type="default"
                    stylingMode="outlined"
                    onClick={() => navigate(`/my-stores/${store.id}/products`)}
                  />
                  <Button
                    text="Редактировать"
                    type="default"
                    stylingMode="outlined"
                    onClick={() => navigate(`/my-stores/${store.id}/edit`)}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
