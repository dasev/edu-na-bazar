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
  store_id: undefined,
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
    const currentState = get()
    const currentValue = currentState[key]
    
    console.log(`🔧 setFilter called:`, { key, from: currentValue, to: value })
    
    // Если меняем skip, не сбрасываем его
    if (key === 'skip') {
      console.log('✅ Setting skip without reset')
      set({ [key]: value })
      return
    }
    
    // Проверяем реальное изменение (учитываем undefined и null как одинаковые)
    const hasChanged = (currentValue !== value) && 
                       !(currentValue == null && value == null)
    
    if (hasChanged) {
      console.log('✅ Value changed, updating and resetting skip to 0')
      set({ [key]: value, skip: 0 })
    } else {
      console.log('⏭️ Value not changed, skipping update')
    }
  },

  resetFilters: () => {
    set(defaultFilters)
  },

  getActiveFiltersCount: () => {
    const state = get()
    let count = 0
    
    if (state.category_id !== undefined && state.category_id !== null) count++
    if (state.store_id !== undefined && state.store_id !== null) count++
    if (state.min_price !== undefined && state.min_price !== null) count++
    if (state.max_price !== undefined && state.max_price !== null) count++
    if (state.min_rating !== undefined && state.min_rating !== null) count++
    if (state.in_stock !== undefined && state.in_stock !== null) count++
    if (state.search !== undefined && state.search !== null && state.search !== '') count++
    
    return count
  },
}))
