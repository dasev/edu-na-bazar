/**
 * Cart API service
 */
import apiClient from '../client'
import type { Cart } from '../types'

export const cartApi = {
  /**
   * Получить корзину пользователя
   */
  getCart: async (): Promise<Cart> => {
    const response = await apiClient.get('/api/cart')
    return response.data
  },

  /**
   * Добавить товар в корзину
   */
  addToCart: async (productId: string, quantity: number = 1): Promise<{ message: string; item_id: string }> => {
    const response = await apiClient.post('/api/cart/items', {
      product_id: productId,
      quantity,
    })
    return response.data
  },

  /**
   * Обновить количество товара в корзине
   */
  updateCartItem: async (itemId: string, quantity: number): Promise<{ message: string }> => {
    const response = await apiClient.put(`/api/cart/items/${itemId}`, { quantity })
    return response.data
  },

  /**
   * Удалить товар из корзины
   */
  removeFromCart: async (itemId: string): Promise<void> => {
    await apiClient.delete(`/api/cart/items/${itemId}`)
  },

  /**
   * Очистить корзину
   */
  clearCart: async (): Promise<void> => {
    await apiClient.delete('/api/cart')
  },
}
