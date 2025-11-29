import { useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import CustomStore from 'devextreme/data/custom_store'
import { apiClient } from '../../../api/client'
import toast from 'react-hot-toast'

export interface User {
  id: number
  phone: string
  email?: string
  full_name: string
  address?: string
  is_active: boolean
  is_verified: boolean
  is_email_verified?: boolean
  is_phone_verified?: boolean
  is_moderator: boolean
  stores_count: number
  products_count: number
  orders_count: number
  created_at: string
}

export interface Stats {
  total_users: number
  active_users: number
  verified_users: number
  moderators: number
  total_stores: number
  total_products: number
  total_orders: number
}

export const useUsersData = (filterValue: 'all' | 'active' | 'moderators') => {
  const queryClient = useQueryClient()

  const { data: stats } = useQuery<Stats>({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const response = await apiClient.get('/api/admin/stats')
      return response.data
    },
  })

  const dataSource = useMemo(() => new CustomStore({
    key: 'id',
    load: async (loadOptions) => {
      const params: any = {
        skip: loadOptions.skip || 0,
        limit: loadOptions.take || 20,
      }

      if (filterValue === 'active') params.is_active = true
      if (filterValue === 'moderators') params.is_moderator = true

      // Глобальный поиск (SearchPanel) - только по текстовым полям
      if (loadOptions.searchValue) {
        params.search = loadOptions.searchValue
      }

      // Обработка фильтров из колонок
      if (loadOptions.filter) {
        console.log('Filter received:', loadOptions.filter)
        const processFilter = (filter: any): void => {
          if (Array.isArray(filter)) {
            if (filter.length === 3 && typeof filter[0] === 'string') {
              // Простой фильтр: ['field', 'operator', 'value']
              const [field, operator, value] = filter
              
              // Текстовые поля - используем search
              if (field === 'phone' || field === 'full_name' || field === 'email') {
                if (!params.search) {
                  params.search = value
                }
              } 
              // Булевы поля
              else if (field === 'is_active' && operator === '=') {
                params.is_active = value
              } else if (field === 'is_moderator' && operator === '=') {
                params.is_moderator = value
              }
              // Числовые поля - добавляем как отдельные параметры
              else if (field === 'id') {
                if (operator === '=') params.id = value
                else if (operator === '<') params.id_lt = value
                else if (operator === '>') params.id_gt = value
              } else if (field === 'stores_count' || field === 'products_count') {
                // Пока не поддерживаем фильтрацию по счетчикам
              }
              
              console.log('Processed filter:', { field, operator, value })
            } else {
              // Составной фильтр с логическими операторами
              filter.forEach((item: any) => {
                if (Array.isArray(item)) {
                  processFilter(item)
                }
              })
            }
          }
        }
        processFilter(loadOptions.filter)
      }

      if (loadOptions.sort && Array.isArray(loadOptions.sort) && loadOptions.sort.length > 0) {
        const sortInfo = loadOptions.sort[0] as any
        params.sort = sortInfo.selector + ',' + (sortInfo.desc ? 'desc' : 'asc')
      }

      console.log('Request params:', params)
      const response = await apiClient.get('/api/admin/users', { params })
      return {
        data: response.data.data,
        totalCount: response.data.totalCount
      }
    }
  }), [filterValue])

  const updateMutation = useMutation({
    mutationFn: async (data: { id: number; updates: Partial<User> }) => {
      await apiClient.patch(`/api/admin/users/${data.id}`, data.updates)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] })
      toast.success('Пользователь обновлен')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/api/admin/users/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] })
      toast.success('Пользователь удален')
    },
  })

  return {
    stats,
    dataSource,
    updateMutation,
    deleteMutation
  }
}
