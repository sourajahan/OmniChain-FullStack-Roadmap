import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'
import { AuthProvider } from '../hooks/AuthProvider'
import { AppRoutes } from '../App'
import { tokenStore } from '../api/client'

describe('Auth Routing & Login Page', () => {
  beforeEach(() => {
    tokenStore.clear()
  })

  it('redirects unauthenticated users to /login with semantic landmarks', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </MemoryRouter>,
    )

    expect(screen.getByRole('banner')).toBeInTheDocument()
    expect(screen.getByRole('main')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /Sign in to OmniStore/i })).toBeInTheDocument()
  })

  it('toggles between login and register modes', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </MemoryRouter>,
    )

    await user.click(screen.getByRole('button', { name: /Create an account/i }))
    expect(screen.getByRole('heading', { name: /Create an account/i })).toBeInTheDocument()
    expect(screen.getByLabelText(/Full name/i)).toBeInTheDocument()
  })
})
