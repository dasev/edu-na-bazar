import { apiClient } from '../api/client'

export const trackEvent = async (
  eventType: 'product_click' | 'add_to_cart_click' | 'checkout_start' | 'checkout_complete',
  productId?: number,
  orderId?: number,
  metadata?: string
) => {
  try {
    const response = await apiClient.post('/api/events/track', {
      event_type: eventType,
      product_id: productId,
      order_id: orderId,
      metadata
    })
    
    // Сохраняем session_id в cookies если вернулся
    if (response.data.session_id) {
      document.cookie = `session_id=${response.data.session_id}; path=/; max-age=31536000`
    }
  } catch (error) {
    console.log('Failed to track event:', error)
  }
}
