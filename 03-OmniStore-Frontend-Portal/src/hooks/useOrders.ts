import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import * as ordersApi from '../api/orders'
import type { CreateOrderInput, OrderStatus } from '../types/domain'

export const ORDERS_QUERY_KEY = ['orders'] as const

export function useOrdersQuery(status: OrderStatus | 'all' = 'all') {
  return useQuery({
    queryKey: [...ORDERS_QUERY_KEY, status],
    queryFn: () => ordersApi.fetchOrders(status),
  })
}

export function useCreateOrderMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateOrderInput) => ordersApi.createOrder(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ORDERS_QUERY_KEY })
    },
  })
}

export function useUpdateOrderStatusMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ orderId, status }: { orderId: string; status: OrderStatus }) =>
      ordersApi.updateOrderStatus(orderId, status),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ORDERS_QUERY_KEY })
    },
  })
}
