import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface GeoAnalyticsData {
  conversion_by_city: Array<{
    city: string
    orders: number
    users: number
    conversion_rate: number
  }>
  orders_by_city: Array<{
    city: string
    orders_count: number
  }>
  revenue_by_city: Array<{
    city: string
    revenue: number
  }>
  top_cities: Array<{
    city: string
    orders: number
    revenue: number
    users: number
  }>
}

export const useGeoAnalytics = (enabled: boolean = false) => {
  return useQuery<GeoAnalyticsData>({
    queryKey: ['analytics-geography'],
    queryFn: async () => {
      const response = await apiClient.get('/api/analytics/geography')
      return response.data
    },
    enabled,
  })
}
