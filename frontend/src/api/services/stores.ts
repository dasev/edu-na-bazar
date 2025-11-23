/**
 * Stores API service
 */
import apiClient from '../client'
import type { Store, StoreWithDistance } from '../types'

export const storesApi = {
  /**
   * Получить все магазины
   */
  getStores: async (): Promise<Store[]> => {
    const response = await apiClient.get('/api/stores')
    return response.data
  },

  /**
   * Получить ближайшие магазины
   */
  getNearbyStores: async (
    lat: number,
    lon: number,
    radiusKm: number = 5
  ): Promise<StoreWithDistance[]> => {
    const response = await apiClient.get('/api/stores/nearby', {
      params: { lat, lon, radius_km: radiusKm },
    })
    return response.data
  },

  /**
   * Получить магазин по ID
   */
  getStore: async (id: string): Promise<Store> => {
    const response = await apiClient.get(`/api/stores/${id}`)
    return response.data
  },
}
