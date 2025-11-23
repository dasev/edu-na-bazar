/**
 * Categories API service
 */
import apiClient from '../client'
import type { Category } from '../types'

export const categoriesApi = {
  /**
   * Получить все категории
   */
  getCategories: async (): Promise<Category[]> => {
    try {
      const response = await apiClient.get('/api/categories')
      return response.data || []
    } catch (error) {
      console.error('Error fetching categories:', error)
      return []
    }
  },

  /**
   * Получить категорию по ID
   */
  getCategory: async (id: string): Promise<Category> => {
    const response = await apiClient.get(`/api/categories/${id}`)
    return response.data
  },

  /**
   * Создать категорию (только для админов)
   */
  createCategory: async (data: Partial<Category>): Promise<Category> => {
    const response = await apiClient.post('/api/categories', data)
    return response.data
  },

  /**
   * Обновить категорию (только для админов)
   */
  updateCategory: async (id: string, data: Partial<Category>): Promise<Category> => {
    const response = await apiClient.put(`/api/categories/${id}`, data)
    return response.data
  },

  /**
   * Удалить категорию (только для админов)
   */
  deleteCategory: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/categories/${id}`)
  },
}
