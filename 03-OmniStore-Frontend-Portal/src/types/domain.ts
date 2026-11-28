export type UserRole = 'customer' | 'warehouse' | 'admin'

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
}

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
}

export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'

export interface OrderItem {
  id: string
  product_sku: string
  product_name: string
  quantity: number
  unit_price: string
}

export interface Order {
  id: string
  customer_id: string
  status: OrderStatus
  total_amount: string
  created_at: string
  items: OrderItem[]
}

export interface CreateOrderItemInput {
  product_sku: string
  product_name: string
  quantity: number
  unit_price: number
}

export interface CreateOrderInput {
  items: CreateOrderItemInput[]
}
