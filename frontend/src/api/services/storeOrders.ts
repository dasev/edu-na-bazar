/**
 * API для работы с заказами магазина
 */
import apiClient from '../client'
import type { OrderListResponse, Order } from '../types'

export const storeOrdersApi = {
  /**
   * Получить заказы магазина
   */
  getStoreOrders: async (
    storeId: number,
    params?: {
      status?: string
      skip?: number
      limit?: number
    }
  ): Promise<OrderListResponse> => {
    const response = await apiClient.get(`/api/my-stores/${storeId}/orders`, { params })
    return response.data
  },

  /**
   * Обновить статус заказа
   */
  updateOrderStatus: async (
    storeId: number,
    orderId: number,
    status: string
  ): Promise<Order> => {
    const response = await apiClient.put(
      `/api/my-stores/${storeId}/orders/${orderId}/status`,
      { status }
    )
    return response.data
  },
}
