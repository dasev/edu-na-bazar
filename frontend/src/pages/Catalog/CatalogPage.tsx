import { useQuery } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { useMemo, useEffect, useState } from 'react'
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
  const [allProducts, setAllProducts] = useState<any[]>([])
  
  // Применяем фильтр по магазину из URL
  useEffect(() => {
    const storeId = searchParams.get('store_id')
    if (storeId) {
      filtersStore.setFilter('store_id', parseInt(storeId))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams])
  
  // Извлекаем только данные фильтров (без функций) и мемоизируем
  const filters = useMemo(() => ({
    category_id: filtersStore.category_id,
    store_id: filtersStore.store_id,
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
    filtersStore.store_id,
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
    queryFn: () => {
      console.log('📡 Fetching products with filters:', filters)
      return productsApi.getProducts(filters)
    },
  })
  
  const meta = productsData?.meta
  
  // Логируем результаты
  useEffect(() => {
    if (productsData) {
      console.log('📦 Products received:', {
        count: productsData.data?.length || 0,
        total: meta?.total || 0,
        skip: filters.skip,
        limit: filters.limit
      })
    }
  }, [productsData, meta, filters.skip, filters.limit])
  
  // Накапливаем товары при загрузке новых или сбрасываем при изменении фильтров
  useEffect(() => {
    if (productsData?.data) {
      const skip = filters.skip || 0
      console.log('🔄 Updating allProducts:', { skip, newCount: productsData.data.length })
      if (skip === 0) {
        // Сброс фильтров - показываем только новые товары
        console.log('✅ Setting allProducts to new data')
        setAllProducts(productsData.data)
      } else {
        // Добавляем к существующим
        console.log('➕ Appending to existing products')
        setAllProducts(prev => [...prev, ...productsData.data])
      }
    }
  }, [productsData, filters.skip])
  
  const handleLoadMore = () => {
    const skip = filters.skip || 0
    const limit = filters.limit || 20
    console.log('🔄 Load More clicked:', { skip, limit, total: meta?.total, hasMore })
    if (meta && skip + limit < meta.total) {
      console.log('✅ Loading more products, new skip:', skip + limit)
      filtersStore.setFilter('skip', skip + limit)
    } else {
      console.log('❌ No more products to load')
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
                {allProducts.length > 0 && (
                  <span className="catalog-page__showing">
                    {' '}(показано {allProducts.length})
                  </span>
                )}
              </span>
              {isLoading && <span style={{ marginLeft: '10px', color: '#667eea' }}>⏳ Загрузка...</span>}
            </div>
            
            {isLoading && allProducts.length === 0 ? (
              <ProductCardSkeletonGrid count={8} />
            ) : allProducts.length === 0 ? (
              <div className="catalog-page__empty">
                <h3>Товары не найдены</h3>
                <p>Попробуйте изменить фильтры</p>
              </div>
            ) : (
              <>
                <div className="catalog-page__grid">
                  {allProducts.map((product: any) => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>
                
                {hasMore && (
                  <div className="catalog-page__load-more">
                    <Button
                      text={isLoading ? "Загрузка..." : "Показать еще"}
                      type="default"
                      stylingMode="outlined"
                      onClick={handleLoadMore}
                      disabled={isLoading}
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
