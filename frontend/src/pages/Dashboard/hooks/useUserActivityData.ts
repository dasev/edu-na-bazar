import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../../../api/client'

export interface UserActivityStats {
  date: string
  new_users: number
  active_users: number
  orders_made: number
}

export interface UserActivityData {
  total_users: number
  active_today: number
  new_this_month: number
  retention_rate: number
  daily_stats: UserActivityStats[]
  users_by_registration_source: Array<{
    source: string
    count: number
  }>
  top_active_users: Array<{
    name: string
    orders_count: number
  }>
}

export const useUserActivityData = (days: number = 30, enabled: boolean = false) => {
  return useQuery<UserActivityData>({
    queryKey: ['analytics-user-activity', days],
    queryFn: async () => {
      const response = await apiClient.get(`/api/analytics/user-activity?days=${days}`)
      return response.data
    },
    enabled,
  })
}
