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

const sortOptions = [
  { id: 'created_at', name: 'По новизне' },
  { id: 'price', name: 'По цене' },
  { id: 'rating', name: 'По рейтингу' },
  { id: 'name', name: 'По названию' },
]

const sortOrderOptions = [
  { id: 'desc', name: 'По убыванию' },
  { id: 'asc', name: 'По возрастанию' },
]

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
    min_price,
    max_price,
    min_rating,
    in_stock,
    sort_by,
    sort_order,
    setFilter,
    resetFilters,
    getActiveFiltersCount,
  } = useFiltersStore()

  const { data: categories = [], isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.getCategories,
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
            {!categoriesLoading && ` (${categoriesWithAll.length} шт.)`}
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
                  {item.icon && <span>{item.icon}</span>}
                  <span>{item.name}</span>
                </div>
              )
            }}
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

        {/* Сортировка */}
        <div className="filter-section">
          <label className="filter-label">Сортировка</label>
          <SelectBox
            dataSource={sortOptions}
            value={sort_by}
            onValueChanged={(e) => {
              setFilter('sort_by', e.value)
              setFilter('skip', 0) // Сбрасываем пагинацию
            }}
            displayExpr="name"
            valueExpr="id"
            width="100%"
          />
        </div>

        {/* Порядок сортировки */}
        <div className="filter-section">
          <label className="filter-label">Порядок</label>
          <SelectBox
            dataSource={sortOrderOptions}
            value={sort_order}
            onValueChanged={(e) => {
              setFilter('sort_order', e.value)
              setFilter('skip', 0) // Сбрасываем пагинацию
            }}
            displayExpr="name"
            valueExpr="id"
            width="100%"
          />
        </div>
      </div>
    </div>
  )
}
