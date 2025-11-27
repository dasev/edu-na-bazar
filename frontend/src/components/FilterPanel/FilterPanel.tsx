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

  // Используем категории как есть, без добавления "Все категории"
  const categoriesWithAll = Array.isArray(categories) ? categories : []

  return (
    <div className="filter-panel">
      <div className="filter-panel__content">
        {/* Категория */}
        <div className="filter-section">
          <label className="filter-label">
            Категория {categoriesLoading && '(загрузка...)'}
          </label>
          <SelectBox
            dataSource={categoriesWithAll}
            value={category_id ?? null}
            onValueChanged={(e) => {
              console.log('🔄 Category changed:', { from: category_id, to: e.value, event: e.event })
              const newValue = (e.value === null || e.value === undefined) ? undefined : e.value
              console.log('➡️ Setting category_id to:', newValue)
              setFilter('category_id', newValue)
            }}
            displayExpr="name"
            valueExpr="id"
            placeholder="Все категории"
            showClearButton={true}
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
            value={store_id ?? null}
            onValueChanged={(e) => {
              console.log('🏪 Store changed:', { from: store_id, to: e.value, event: e.event })
              const newValue = (e.value === null || e.value === undefined) ? undefined : e.value
              console.log('➡️ Setting store_id to:', newValue)
              setFilter('store_id', newValue)
            }}
            dataSource={stores}
            displayExpr="name"
            valueExpr="id"
            placeholder="Все магазины"
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
            value={min_rating ?? null}
            onValueChanged={(e) => {
              console.log('⭐ Rating changed:', { from: min_rating, to: e.value, event: e.event })
              const newValue = (e.value === null || e.value === undefined) ? undefined : e.value
              console.log('➡️ Setting min_rating to:', newValue)
              setFilter('min_rating', newValue)
            }}
            displayExpr="name"
            valueExpr="id"
            placeholder="Любой рейтинг"
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
            }}
          />
        </div>

        {/* Кнопка сброса фильтров */}
        {activeFiltersCount > 0 && (
          <div className="filter-section" style={{ marginTop: '16px' }}>
            <Button
              text={`Сбросить фильтры (${activeFiltersCount})`}
              stylingMode="outlined"
              type="normal"
              onClick={() => {
                console.log('🔄 Resetting all filters')
                resetFilters()
              }}
              width="100%"
            />
          </div>
        )}
      </div>
    </div>
  )
}
