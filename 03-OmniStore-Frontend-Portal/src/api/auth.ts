import { apiRequest, tokenStore } from './client'
import type { TokenPair, User } from '../types/domain'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  full_name: string
}

export async function login(payload: LoginPayload): Promise<TokenPair> {
  const tokens = await apiRequest<TokenPair>(
    '/api/v1/auth/login',
    { method: 'POST', body: JSON.stringify(payload) },
    false,
  )
  tokenStore.setTokens(tokens)
  return tokens
}

export async function register(payload: RegisterPayload): Promise<User> {
  return apiRequest<User>(
    '/api/v1/auth/register',
    { method: 'POST', body: JSON.stringify(payload) },
    false,
  )
}

export async function fetchCurrentUser(): Promise<User> {
  return apiRequest<User>('/api/v1/auth/me')
}

export async function logout(): Promise<void> {
  const refreshToken = tokenStore.getRefreshToken()
  try {
    if (refreshToken) {
      await apiRequest<void>(
        '/api/v1/auth/logout',
        { method: 'POST', body: JSON.stringify({ refresh_token: refreshToken }) },
        false,
      )
    }
  } finally {
    tokenStore.clear()
  }
}
