import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import { AppRoutes } from '../App'
import * as mediaApi from '../api/media'

vi.mock('../api/media')

function renderApp(initialPath = '/') {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[initialPath]}>
        <AppRoutes />
      </MemoryRouter>
    </QueryClientProvider>,
  )
}

describe('SearchMedia Frontend', () => {
  it('renders search results and X-Cache badge', async () => {
    vi.mocked(mediaApi.searchMedia).mockResolvedValueOnce({
      items: [
        {
          id: '1',
          title: 'Redis Cache ADR',
          tags: ['redis', 'devops'],
          original_filename: 'adr.txt',
          stored_filename: '1.txt',
          content_type: 'text/plain',
          size_bytes: 1024,
          created_at: '2026-01-01T00:00:00Z',
        },
      ],
      total: 1,
      page: 1,
      limit: 6,
      pages: 1,
      cacheStatus: 'HIT',
    })

    renderApp('/')
    expect(await screen.findByText(/Redis Cache ADR/i)).toBeInTheDocument()
    expect(screen.getByText(/X-Cache: HIT/i)).toBeInTheDocument()
  })

  it('validates upload form before submitting', async () => {
    const user = userEvent.setup()
    renderApp('/upload')

    await user.click(screen.getByRole('button', { name: /Upload Asset/i }))
    expect(screen.getByRole('alert')).toHaveTextContent(/Title must be at least 2 characters/i)
  })
})
