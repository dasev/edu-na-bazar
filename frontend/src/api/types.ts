/**
 * TypeScript типы для API
 */

// Category
export interface Category {
  id: string
  name: string
  slug: string
  icon?: string
  description?: string
  parent_id?: string
  sort_order: number
  created_at: string
  updated_at: string
}

// Product
export interface Product {
  id: string
  name: string
  slug: string
  description?: string
  price: number
  old_price?: number
  image?: string
  images?: string[]
  category_id: string
  rating: number
  reviews_count: number
  in_stock: boolean
  stock_quantity: number
  unit: string
  meta_title?: string
  meta_description?: string
  created_at: string
  updated_at: string
}

export interface ProductFilters {
  category_id?: string
  min_price?: number
  max_price?: number
  min_rating?: number
  in_stock?: boolean
  search?: string
  sort_by?: 'price' | 'rating' | 'created_at' | 'name'
  sort_order?: 'asc' | 'desc'
  skip?: number
  limit?: number
}

export interface ProductListResponse {
  data: Product[]
  meta: {
    total: number
    skip: number
    limit: number
    page: number
    pages: number
  }
}

// Store
export interface Store {
  id: string
  name: string
  address: string
  phone?: string
  email?: string
  working_hours?: string
  description?: string
  location: {
    type: 'Point'
    coordinates: [number, number] // [longitude, latitude]
  }
  image?: string
  is_active: string
  created_at: string
  updated_at: string
}

export interface StoreWithDistance extends Store {
  distance_km: number
}

// Cart
export interface CartItem {
  id: string
  product_id: string
  quantity: number
  created_at: string
  updated_at: string
  product_name: string
  product_price: number
  product_image?: string
  product_in_stock: boolean
  subtotal: number
}

export interface Cart {
  items: CartItem[]
  total: number
  items_count: number
}

// Order
export interface OrderItem {
  product_id: string
  quantity: number
}

export interface OrderItemResponse {
  id: string
  order_id: string
  product_id: string
  quantity: number
  price: number
  product_name: string
  product_image?: string
  created_at: string
}

export interface Order {
  id: string
  user_id: string
  status: string
  total: number
  delivery_address: string
  delivery_time?: string
  delivery_comment?: string
  payment_method: string
  payment_status: string
  contact_phone: string
  contact_name: string
  comment?: string
  created_at: string
  updated_at: string
  completed_at?: string
  items: OrderItemResponse[]
}

export interface OrderCreate {
  items: OrderItem[]
  delivery_address: string
  delivery_time?: string
  delivery_comment?: string
  payment_method: string
  contact_phone: string
  contact_name: string
  comment?: string
}

export interface OrderListResponse {
  data: Order[]
  meta: {
    total: number
    skip: number
    limit: number
    page: number
    pages: number
  }
}

// Auth
export interface User {
  id: string
  phone: string
  full_name: string
  email?: string
  is_verified: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}
