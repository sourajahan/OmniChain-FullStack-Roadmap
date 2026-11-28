import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { OrderList } from '../components/OrderList'
import { AuthContext } from '../hooks/authContext'
import * as ordersApi from '../api/orders'

vi.mock('../api/orders')

function renderWithProviders(role: 'customer' | 'warehouse' = 'warehouse') {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })

  return render(
    <QueryClientProvider client={queryClient}>
      <AuthContext.Provider
        value={{
          user: {
            id: 'u-1',
            email: 'ops@omnistore.dev',
            full_name: 'Ops Manager',
            role,
            is_active: true,
          },
          isLoading: false,
          isAuthenticated: true,
          login: vi.fn(),
          register: vi.fn(),
          logout: vi.fn(),
        }}
      >
        <OrderList />
      </AuthContext.Provider>
    </QueryClientProvider>,
  )
}

describe('OrderList with TanStack Query', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders fetched orders and RBAC action for warehouse role', async () => {
    vi.mocked(ordersApi.fetchOrders).mockResolvedValueOnce({
      items: [
        {
          id: 'ord-12345678',
          customer_id: 'u-2',
          status: 'pending',
          total_amount: '149.90',
          created_at: '2026-01-01T00:00:00Z',
          items: [
            {
              id: 'item-1',
              product_sku: 'KB-01',
              product_name: 'Mechanical Keyboard',
              quantity: 1,
              unit_price: '149.90',
            },
          ],
        },
      ],
      total: 1,
      limit: 20,
      offset: 0,
    })

    renderWithProviders('warehouse')

    expect(await screen.findByText(/Mechanical Keyboard/i)).toBeInTheDocument()
    expect(screen.getByText(/\$149\.90/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Mark as confirmed/i })).toBeInTheDocument()
  })

  it('shows error state with retry button when API fails', async () => {
    vi.mocked(ordersApi.fetchOrders).mockRejectedValueOnce(new Error('Network down'))

    renderWithProviders('customer')

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/Network down/i)
    })
    expect(screen.getByRole('button', { name: /Retry/i })).toBeInTheDocument()
  })
})
