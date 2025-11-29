import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface FinancialStats {
  date: string
  revenue: number
  orders_count: number
  avg_order_value: number
}

export interface FinancialData {
  total_revenue: number
  avg_order_value: number
  daily_stats: FinancialStats[]
  top_products_by_revenue: Array<{
    name: string
    revenue: number
  }>
  revenue_by_category: Array<{
    name: string
    revenue: number
  }>
}

export const useFinancialData = (days: number = 30, enabled: boolean = false) => {
  return useQuery<FinancialData>({
    queryKey: ['analytics-financial', days],
    queryFn: async () => {
      const response = await apiClient.get(`/api/analytics/financial?days=${days}`)
      return response.data
    },
    enabled, // Загружаем только когда enabled=true
  })
}
