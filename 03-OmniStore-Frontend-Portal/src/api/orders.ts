import { apiRequest } from './client'
import type { PaginatedResponse } from '../types/api'
import type { CreateOrderInput, Order, OrderStatus } from '../types/domain'

export async function fetchOrders(status?: OrderStatus | 'all'): Promise<PaginatedResponse<Order>> {
  const query = status && status !== 'all' ? `?status=${encodeURIComponent(status)}` : ''
  return apiRequest<PaginatedResponse<Order>>(`/api/v1/orders${query}`)
}

export async function createOrder(payload: CreateOrderInput): Promise<Order> {
  return apiRequest<Order>('/api/v1/orders', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
  return apiRequest<Order>(`/api/v1/orders/${encodeURIComponent(orderId)}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  })
}
