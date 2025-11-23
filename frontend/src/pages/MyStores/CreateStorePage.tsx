/**
 * Страница создания магазина с интеграцией DaData
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import { TextArea } from 'devextreme-react/text-area';
import { Autocomplete } from 'devextreme-react/autocomplete';
import { useAuthStore } from '../../store/authStore';
import { myStoresApi } from '../../api/services/myStores';
import './CreateStorePage.css';

const DADATA_API_KEY = 'e76739998f03541266e5b2f288d0d1c8b5d2f876';
const DADATA_SUGGEST_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party';

interface DaDataResponse {
  suggestions: Array<{
    value: string;
    data: {
      inn: string;
      kpp?: string;
      ogrn?: string;
      name: {
        full_with_opf: string;
        short_with_opf: string;
      };
      address: {
        value: string;
      };
      management?: {
        name: string;
        post: string;
      };
    };
  }>;
}

export const CreateStorePage = () => {
  const navigate = useNavigate();
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
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [searchValue, setSearchValue] = useState('');

  // Поиск организаций через DaData (автокомплит)
  const handleSearchOrganizations = async (query: string) => {
    if (!query || query.length < 3) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await fetch(DADATA_SUGGEST_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${DADATA_API_KEY}`,
        },
        body: JSON.stringify({ query, count: 10 }),
      });

      if (!response.ok) {
        throw new Error('Ошибка запроса к DaData');
      }

      const data: DaDataResponse = await response.json();
      setSuggestions(data.suggestions || []);
    } catch (err: any) {
      console.error('Ошибка поиска:', err);
      setSuggestions([]);
    }
  };

  // Выбор организации из списка
  const handleSelectOrganization = (suggestion: any) => {
    const org = suggestion.data;

    // Автозаполнение всех полей
    setInn(org.inn);
    setLegalName(org.name.full_with_opf);
    setName(org.name.short_with_opf);
    setAddress(org.address.value);
    setKpp(org.kpp || '');
    setOgrn(org.ogrn || '');
    setSearchValue(suggestion.value);

    // Очищаем подсказки
    setSuggestions([]);
  };

  // Создание магазина
  const handleCreateStore = async () => {
    setError('');

    // Валидация
    if (!inn || !name || !legalName || !address) {
      setError('Заполните обязательные поля');
      return;
    }

    setLoading(true);

    try {
      await myStoresApi.createStore({
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

      // Успешно создан - переходим к списку магазинов
      navigate('/my-stores');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания магазина');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
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
          <h1>Создать магазин</h1>
        </div>

        <div className="create-store-form">
          {/* Поиск организации */}
          <div className="form-section">
            <h2><span className="section-icon">🔍</span> Поиск организации</h2>
            <p className="form-section-description">
              Начните вводить название, ИНН или адрес организации
            </p>

            <div className="form-group">
              <label className="form-label">Поиск организации *</label>
              <Autocomplete
                value={searchValue}
                onValueChanged={(e) => {
                  setSearchValue(e.value);
                  handleSearchOrganizations(e.value);
                }}
                dataSource={suggestions}
                valueExpr="value"
                displayExpr={(item: any) => {
                  if (!item) return '';
                  return `${item.value} (ИНН: ${item.data.inn})`;
                }}
                onItemClick={(e) => handleSelectOrganization(e.itemData)}
                placeholder="Например: ООО Ромашка, 7707083893, г. Москва"
                disabled={loading}
                stylingMode="outlined"
                minSearchLength={3}
                searchTimeout={500}
                showClearButton={true}
              />
              <div className="form-hint">
                💡 Введите минимум 3 символа для поиска
              </div>
            </div>
          </div>

          {/* Основные данные */}
          <div className="form-section">
            <h2><span className="section-icon">📋</span> Основные данные</h2>

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
              text={loading ? 'Создание...' : 'Создать магазин'}
              type="default"
              stylingMode="contained"
              onClick={handleCreateStore}
              disabled={loading || !inn || !name || !legalName || !address}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
