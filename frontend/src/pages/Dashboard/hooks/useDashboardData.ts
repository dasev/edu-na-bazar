import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface DailyStats {
  date: string
  products: number
  stores: number
  orders: number
  users: number
}

export interface AnalyticsData {
  total_products: number
  total_stores: number
  total_orders: number
  total_users: number
  daily_stats: DailyStats[]
  top_categories: Array<{
    name: string
    icon: string
    count: number
  }>
}

export const useDashboardData = (days: number = 30) => {
  return useQuery<AnalyticsData>({
    queryKey: ['analytics-dashboard', days],
    queryFn: async () => {
      const response = await apiClient.get(`/api/analytics/dashboard?days=${days}`)
      return response.data
    },
  })
}
