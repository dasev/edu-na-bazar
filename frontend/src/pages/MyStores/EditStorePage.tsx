/**
 * Страница редактирования магазина
 */
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import { TextArea } from 'devextreme-react/text-area';
import { useAuthStore } from '../../store/authStore';
import { myStoresApi } from '../../api/services/myStores';
import './CreateStorePage.css';

export const EditStorePage = () => {
  const navigate = useNavigate();
  const { storeId } = useParams<{ storeId: string }>();
  const queryClient = useQueryClient();
  const { isAuthenticated } = useAuthStore();

  // Автоматический редирект если не авторизован
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  // Форма
  const [inn, setInn] = useState('');
  const [name, setName] = useState('');
  const [legalName, setLegalName] = useState('');
  const [kpp, setKpp] = useState('');
  const [ogrn, setOgrn] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [description, setDescription] = useState('');

  // Состояние
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Загрузка данных магазина
  const { data: store, isLoading } = useQuery({
    queryKey: ['store', storeId],
    queryFn: async () => {
      const store = await myStoresApi.getStore(storeId!);
      return store;
    },
    enabled: !!storeId,
  });

  // Заполнение формы при загрузке данных
  useEffect(() => {
    if (store) {
      setInn(store.inn || '');
      setName(store.name || '');
      setLegalName(store.legal_name || '');
      setKpp(store.kpp || '');
      setOgrn(store.ogrn || '');
      setAddress(store.address || '');
      setPhone(store.phone || '');
      setEmail(store.email || '');
      setDescription(store.description || '');
    }
  }, [store]);

  // Обновление магазина
  const handleUpdateStore = async () => {
    setError('');

    // Проверка авторизации
    const token = localStorage.getItem('auth_token');
    if (!token) {
      setError('Ошибка авторизации. Пожалуйста, обновите страницу (F5) и попробуйте снова.');
      return;
    }

    // Валидация
    if (!inn || !name || !legalName || !address) {
      setError('Заполните обязательные поля');
      return;
    }

    setLoading(true);

    try {
      await myStoresApi.updateStore(storeId!, {
        inn,
        name,
        legal_name: legalName,
        address,
        phone: phone || undefined,
        email: email || undefined,
        description: description || undefined,
        kpp: kpp || undefined,
        ogrn: ogrn || undefined,
      });

      // Инвалидируем кэш
      await queryClient.invalidateQueries({ queryKey: ['my-stores'] });
      await queryClient.invalidateQueries({ queryKey: ['store', storeId] });

      // Успешно обновлен - переходим к списку магазинов
      navigate('/my-stores');
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Ошибка авторизации. Пожалуйста, обновите страницу (F5) и попробуйте снова.');
      } else {
        setError(err.response?.data?.detail || 'Ошибка обновления магазина');
      }
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated || isLoading) {
    return null;
  }

  return (
    <div className="create-store-page">
      <div className="create-store-container">
        <div className="create-store-header">
          <Button
            icon="back"
            text="Назад"
            stylingMode="text"
            onClick={() => navigate('/my-stores')}
          />
          <h1>Редактировать магазин</h1>
        </div>

        <div className="create-store-form">
          {/* Основные данные */}
          <div className="form-section">
            <h2><span className="section-icon">📋</span> Основные данные</h2>

            <div className="form-group">
              <label className="form-label">ИНН *</label>
              <TextBox
                value={inn}
                onValueChanged={(e) => setInn(e.value)}
                placeholder="1234567890"
                disabled={loading}
                stylingMode="outlined"
                readOnly
              />
            </div>

            <div className="form-group">
              <label className="form-label">Название магазина *</label>
              <TextBox
                value={name}
                onValueChanged={(e) => setName(e.value)}
                placeholder="ИП Иванов И.И."
                disabled={loading}
                stylingMode="outlined"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Юридическое название *</label>
              <TextBox
                value={legalName}
                onValueChanged={(e) => setLegalName(e.value)}
                placeholder="Индивидуальный предприниматель Иванов Иван Иванович"
                disabled={loading}
                stylingMode="outlined"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">КПП</label>
                <TextBox
                  value={kpp}
                  onValueChanged={(e) => setKpp(e.value)}
                  placeholder="123456789"
                  maxLength={9}
                  disabled={loading}
                  stylingMode="outlined"
                />
              </div>

              <div className="form-group">
                <label className="form-label">ОГРН</label>
                <TextBox
                  value={ogrn}
                  onValueChanged={(e) => setOgrn(e.value)}
                  placeholder="1234567890123"
                  maxLength={15}
                  disabled={loading}
                  stylingMode="outlined"
                />
              </div>
            </div>
          </div>

          {/* Контактные данные */}
          <div className="form-section">
            <h2><span className="section-icon">📞</span> Контактные данные</h2>

            <div className="form-group">
              <label className="form-label">Адрес *</label>
              <TextBox
                value={address}
                onValueChanged={(e) => setAddress(e.value)}
                placeholder="г. Москва, ул. Ленина, д. 1"
                disabled={loading}
                stylingMode="outlined"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Телефон</label>
                <TextBox
                  value={phone}
                  onValueChanged={(e) => setPhone(e.value)}
                  placeholder="+7 (999) 123-45-67"
                  disabled={loading}
                  stylingMode="outlined"
                  mode="tel"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Email</label>
                <TextBox
                  value={email}
                  onValueChanged={(e) => setEmail(e.value)}
                  placeholder="shop@example.com"
                  disabled={loading}
                  stylingMode="outlined"
                  mode="email"
                />
              </div>
            </div>
          </div>

          {/* Описание */}
          <div className="form-section">
            <h2><span className="section-icon">📝</span> Описание</h2>

            <div className="form-group">
              <label className="form-label">Описание магазина</label>
              <TextArea
                value={description}
                onValueChanged={(e) => setDescription(e.value)}
                placeholder="Расскажите о вашем магазине..."
                height={120}
                disabled={loading}
                stylingMode="outlined"
              />
            </div>
          </div>

          {/* Ошибка */}
          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          {/* Кнопки */}
          <div className="form-actions">
            <Button
              text="Отмена"
              stylingMode="outlined"
              onClick={() => navigate('/my-stores')}
              disabled={loading}
            />
            <Button
              text={loading ? 'Сохранение...' : 'Сохранить изменения'}
              type="default"
              stylingMode="contained"
              onClick={handleUpdateStore}
              disabled={loading || !inn || !name || !legalName || !address}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
