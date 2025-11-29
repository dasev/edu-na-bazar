import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface ProductAnalyticsData {
  top_products_by_conversion: Array<{
    id: number
    name: string
    views: number
    orders: number
    conversion_rate: number
  }>
  worst_products_by_conversion: Array<{
    id: number
    name: string
    views: number
    orders: number
    conversion_rate: number
  }>
  locomotive_products: Array<{
    id: number
    name: string
    orders_count: number
    avg_items_in_order: number
  }>
  cross_sell_pairs: Array<{
    product1: string
    product2: string
    frequency: number
  }>
}

export const useProductAnalytics = (enabled: boolean = false) => {
  return useQuery<ProductAnalyticsData>({
    queryKey: ['analytics-products'],
    queryFn: async () => {
      const response = await apiClient.get('/api/analytics/products')
      return response.data
    },
    enabled,
  })
}
