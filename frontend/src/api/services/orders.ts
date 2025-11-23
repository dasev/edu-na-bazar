/**
 * Orders API service
 */
import apiClient from '../client'
import type { Order, OrderCreate, OrderListResponse } from '../types'

export const ordersApi = {
  /**
   * Получить заказы пользователя
   */
  getOrders: async (params?: { status?: string; skip?: number; limit?: number }): Promise<OrderListResponse> => {
    const response = await apiClient.get('/api/orders', { params })
    return response.data
  },

  /**
   * Получить заказ по ID
   */
  getOrder: async (id: string): Promise<Order> => {
    const response = await apiClient.get(`/api/orders/${id}`)
    return response.data
  },

  /**
   * Создать заказ
   */
  createOrder: async (data: OrderCreate): Promise<Order> => {
    const response = await apiClient.post('/api/orders', data)
    return response.data
  },

  /**
   * Обновить статус заказа
   */
  updateOrderStatus: async (id: string, status: string): Promise<Order> => {
    const response = await apiClient.put(`/api/orders/${id}/status`, { status })
    return response.data
  },
}
