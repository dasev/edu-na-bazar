import { useQuery } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { useMemo, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import ProductCard from '../../components/ProductCard/ProductCard'
import FilterPanel from '../../components/FilterPanel/FilterPanel'
import { ProductCardSkeletonGrid } from '../../components/LoadingSkeleton/ProductCardSkeleton'
import { productsApi } from '../../api'
import { useFiltersStore } from '../../store/filtersStore'
import './CatalogPage.css'

export default function CatalogPage() {
  const filtersStore = useFiltersStore()
  const [searchParams] = useSearchParams()
  
  // Применяем фильтр по магазину из URL
  useEffect(() => {
    const storeId = searchParams.get('store_id')
    if (storeId) {
      filtersStore.setFilter('store_id', parseInt(storeId))
    }
  }, [searchParams, filtersStore])
  
  // Извлекаем только данные фильтров (без функций) и мемоизируем
  const filters = useMemo(() => ({
    category_id: filtersStore.category_id,
    min_price: filtersStore.min_price,
    max_price: filtersStore.max_price,
    min_rating: filtersStore.min_rating,
    in_stock: filtersStore.in_stock,
    search: filtersStore.search,
    sort_by: filtersStore.sort_by,
    sort_order: filtersStore.sort_order,
    skip: filtersStore.skip,
    limit: filtersStore.limit,
  }), [
    filtersStore.category_id,
    filtersStore.min_price,
    filtersStore.max_price,
    filtersStore.min_rating,
    filtersStore.in_stock,
    filtersStore.search,
    filtersStore.sort_by,
    filtersStore.sort_order,
    filtersStore.skip,
    filtersStore.limit,
  ])
  
  const { data: productsData, isLoading } = useQuery({
    queryKey: ['products', filters],
    queryFn: () => productsApi.getProducts(filters),
  })
  
  const products = productsData?.data || []
  const meta = productsData?.meta
  
  const handleLoadMore = () => {
    const skip = filters.skip || 0
    const limit = filters.limit || 20
    if (meta && skip + limit < meta.total) {
      filtersStore.setFilter('skip', skip + limit)
    }
  }

  const skip = filters.skip || 0
  const limit = filters.limit || 20
  const hasMore = meta && skip + limit < meta.total

  return (
    <div className="catalog-page">
      <div className="catalog-page__container">
        <div className="catalog-page__content">
          {/* Фильтры */}
          <aside className="catalog-page__filters">
            <FilterPanel />
          </aside>
          
          {/* Товары */}
          <div className="catalog-page__products">
            <div className="catalog-page__toolbar">
              <span>
                Найдено: {meta?.total || 0} товаров
                {products.length > 0 && (
                  <span className="catalog-page__showing">
                    {' '}(показано {skip + 1}-{Math.min(skip + limit, meta?.total || 0)})
                  </span>
                )}
              </span>
              {isLoading && <span style={{ marginLeft: '10px', color: '#667eea' }}>⏳ Загрузка...</span>}
            </div>
            
            {isLoading ? (
              <ProductCardSkeletonGrid count={8} />
            ) : products.length === 0 ? (
              <div className="catalog-page__empty">
                <h3>Товары не найдены</h3>
                <p>Попробуйте изменить фильтры</p>
              </div>
            ) : (
              <>
                <div className="catalog-page__grid">
                  {products.map((product: any) => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>
                
                {hasMore && (
                  <div className="catalog-page__load-more">
                    <Button
                      text="Показать еще"
                      type="default"
                      stylingMode="outlined"
                      onClick={handleLoadMore}
                      width={200}
                    />
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
