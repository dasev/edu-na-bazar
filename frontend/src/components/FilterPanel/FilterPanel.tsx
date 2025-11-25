/**
 * Панель фильтров для каталога товаров
 */
import { useQuery } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { SelectBox } from 'devextreme-react/select-box'
import { NumberBox } from 'devextreme-react/number-box'
import { CheckBox } from 'devextreme-react/check-box'
import { categoriesApi } from '../../api'
import { useFiltersStore } from '../../store/filtersStore'
import './FilterPanel.css'

const ratingOptions = [
  { id: 0, name: 'Любой' },
  { id: 4.5, name: '4.5 и выше' },
  { id: 4.0, name: '4.0 и выше' },
  { id: 3.5, name: '3.5 и выше' },
  { id: 3.0, name: '3.0 и выше' },
]

export default function FilterPanel() {
  const {
    category_id,
    store_id,
    min_price,
    max_price,
    min_rating,
    in_stock,
    setFilter,
    resetFilters,
    getActiveFiltersCount,
  } = useFiltersStore()

  const { data: categories = [], isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.getCategories,
  })

  const { data: stores = [], isLoading: storesLoading } = useQuery({
    queryKey: ['all-stores'],
    queryFn: async () => {
      try {
        // Получаем все магазины через публичный endpoint
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${API_URL}/api/store-owners/all`)
        if (!response.ok) {
          return []
        }
        const data = await response.json()
        return Array.isArray(data) ? data : []
      } catch (error) {
        console.error('Error loading stores:', error)
        return []
      }
    },
  })

  const activeFiltersCount = getActiveFiltersCount()

  // Добавляем опцию "Все категории" в начало списка
  const categoriesWithAll = [
    { id: 'all', name: 'Все категории', icon: '📋' },  // Используем специальное значение
    ...(Array.isArray(categories) ? categories : [])
  ]

  return (
    <div className="filter-panel">
      {activeFiltersCount > 0 && (
        <div className="filter-panel__header">
          <Button
            text={`Сбросить фильтры (${activeFiltersCount})`}
            stylingMode="text"
            onClick={resetFilters}
            width="100%"
          />
        </div>
      )}

      <div className="filter-panel__content">
        {/* Категория */}
        <div className="filter-section">
          <label className="filter-label">
            Категория {categoriesLoading && '(загрузка...)'}
          </label>
          <SelectBox
            dataSource={categoriesWithAll}
            value={category_id || 'all'}
            onValueChanged={(e) => {
              // Если выбрано "Все категории" ('all'), устанавливаем undefined
              setFilter('category_id', e.value === 'all' ? undefined : e.value)
              setFilter('skip', 0) // Сбрасываем пагинацию
            }}
            displayExpr="name"
            valueExpr="id"
            placeholder="Выберите категорию"
            showClearButton={false}
            disabled={categoriesLoading}
            searchEnabled={true}
            searchMode="contains"
            searchExpr="name"
            minSearchLength={0}
            width="100%"
            itemRender={(item) => {
              return (
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {(item.image || item.icon) && <span>{item.image || item.icon}</span>}
                  <span>{item.name}</span>
                </div>
              )
            }}
          />
        </div>

        {/* Магазин */}
        <div className="filter-section">
          <label className="filter-label">
            Магазин {storesLoading && '(загрузка...)'} 
          </label>
          <SelectBox
            value={store_id || null}
            onValueChanged={(e) => {
              setFilter('store_id', e.value)
              setFilter('skip', 0)
            }}
            dataSource={[
              { id: null, name: 'Все магазины' },
              ...stores
            ]}
            displayExpr="name"
            valueExpr="id"
            placeholder="Выберите магазин"
            showClearButton={true}
            disabled={storesLoading}
            searchEnabled={true}
            searchMode="contains"
            searchExpr="name"
            minSearchLength={0}
            width="100%"
          />
        </div>

        {/* Цена */}
        <div className="filter-section">
          <label className="filter-label">Цена, ₽</label>
          <div className="filter-price">
            <NumberBox
              value={min_price}
              onValueChanged={(e) => {
                setFilter('min_price', e.value)
                setFilter('skip', 0) // Сбрасываем пагинацию
              }}
              placeholder="От"
              min={0}
              showClearButton={true}
              valueChangeEvent="keyup" // Применяется при вводе
            />
            <span className="filter-price__separator">—</span>
            <NumberBox
              value={max_price}
              onValueChanged={(e) => {
                setFilter('max_price', e.value)
                setFilter('skip', 0) // Сбрасываем пагинацию
              }}
              placeholder="До"
              min={min_price || 0}
              showClearButton={true}
              valueChangeEvent="keyup" // Применяется при вводе
            />
          </div>
        </div>

        {/* Рейтинг */}
        <div className="filter-section">
          <label className="filter-label">Минимальный рейтинг</label>
          <SelectBox
            dataSource={ratingOptions}
            value={min_rating || 0}
            onValueChanged={(e) => {
              // Если выбрано "Любой" (0), устанавливаем undefined
              setFilter('min_rating', e.value === 0 ? undefined : e.value)
              setFilter('skip', 0) // Сбрасываем пагинацию
            }}
            displayExpr="name"
            valueExpr="id"
            placeholder="Любой"
            showClearButton={true}
            acceptCustomValue={false}
            width="100%"
          />
        </div>

        {/* Наличие */}
        <div className="filter-section">
          <CheckBox
            text="Только в наличии"
            value={in_stock || false}
            onValueChanged={(e) => {
              setFilter('in_stock', e.value ? true : undefined)
              setFilter('skip', 0) // Сбрасываем пагинацию
            }}
          />
        </div>
      </div>
    </div>
  )
}
