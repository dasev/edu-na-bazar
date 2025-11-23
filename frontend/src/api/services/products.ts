/**
 * Products API service
 */
import apiClient from '../client'
import type { Product, ProductFilters, ProductListResponse } from '../types'

export const productsApi = {
  /**
   * Получить список товаров с фильтрами
   */
  getProducts: async (filters?: ProductFilters): Promise<ProductListResponse> => {
    try {
      const response = await apiClient.get('/api/products', { params: filters })
      return response.data || { data: [], meta: { total: 0, skip: 0, limit: 20, page: 1, pages: 0 } }
    } catch (error) {
      console.error('Error fetching products:', error)
      return { data: [], meta: { total: 0, skip: 0, limit: 20, page: 1, pages: 0 } }
    }
  },

  /**
   * Получить товар по ID
   */
  getProduct: async (id: string): Promise<Product> => {
    const response = await apiClient.get(`/api/products/${id}`)
    return response.data
  },

  /**
   * Создать товар (только для админов)
   */
  createProduct: async (data: Partial<Product>): Promise<Product> => {
    const response = await apiClient.post('/api/products', data)
    return response.data
  },

  /**
   * Обновить товар (только для админов)
   */
  updateProduct: async (id: string, data: Partial<Product>): Promise<Product> => {
    const response = await apiClient.put(`/api/products/${id}`, data)
    return response.data
  },

  /**
   * Удалить товар (только для админов)
   */
  deleteProduct: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/products/${id}`)
  },
}
