/**
 * Filters Store (Zustand)
 * Для фильтрации товаров в каталоге
 */
import { create } from 'zustand'
import type { ProductFilters } from '../api/types'

interface FiltersState extends ProductFilters {
  // Actions
  setFilter: (key: keyof ProductFilters, value: any) => void
  resetFilters: () => void
  getActiveFiltersCount: () => number
}

const defaultFilters: ProductFilters = {
  category_id: undefined,
  min_price: undefined,
  max_price: undefined,
  min_rating: undefined,
  in_stock: undefined,
  search: undefined,
  sort_by: 'created_at',
  sort_order: 'desc',
  skip: 0,
  limit: 20,
}

export const useFiltersStore = create<FiltersState>((set, get) => ({
  ...defaultFilters,

  setFilter: (key: keyof ProductFilters, value: any) => {
    set({ [key]: value, skip: 0 }) // Сбрасываем пагинацию при изменении фильтра
  },

  resetFilters: () => {
    set(defaultFilters)
  },

  getActiveFiltersCount: () => {
    const state = get()
    let count = 0
    
    if (state.category_id) count++
    if (state.min_price !== undefined) count++
    if (state.max_price !== undefined) count++
    if (state.min_rating !== undefined) count++
    if (state.in_stock !== undefined) count++
    if (state.search) count++
    
    return count
  },
}))
