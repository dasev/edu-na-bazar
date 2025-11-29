import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface ConversionStats {
  date: string
  views: number
  cart_adds: number
  orders: number
  conversion_rate: number
}

export interface ConversionData {
  total_views: number
  total_cart_adds: number
  total_orders: number
  overall_conversion_rate: number
  cart_to_order_rate: number
  abandoned_carts: number
  daily_stats: ConversionStats[]
  conversion_by_category: Array<{
    name: string
    products: number
    orders: number
    conversion_rate: number
  }>
  // Новые метрики
  product_clicks: number
  add_to_cart_clicks: number
  checkout_starts: number
  avg_time_to_purchase: number
  abandoned_cart_value: number
}

export const useConversionData = (days: number = 30, enabled: boolean = false) => {
  return useQuery<ConversionData>({
    queryKey: ['analytics-conversion', days],
    queryFn: async () => {
      const response = await apiClient.get(`/api/analytics/conversion?days=${days}`)
      return response.data
    },
    enabled,
  })
}
