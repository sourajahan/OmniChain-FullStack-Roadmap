import { useCallback, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import * as authApi from '../api/auth'
import { tokenStore } from '../api/client'
import type { User } from '../types/domain'
import { AuthContext } from './authContext'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(() => Boolean(tokenStore.getAccessToken()))

  useEffect(() => {
    if (!tokenStore.getAccessToken()) return

    let active = true
    authApi
      .fetchCurrentUser()
      .then((profile) => {
        if (active) setUser(profile)
      })
      .catch(() => {
        tokenStore.clear()
        if (active) setUser(null)
      })
      .finally(() => {
        if (active) setIsLoading(false)
      })

    return () => {
      active = false
    }
  }, [])

  const login = useCallback(async (payload: authApi.LoginPayload) => {
    await authApi.login(payload)
    const profile = await authApi.fetchCurrentUser()
    setUser(profile)
  }, [])

  const register = useCallback(async (payload: authApi.RegisterPayload) => {
    await authApi.register(payload)
    await authApi.login({ email: payload.email, password: payload.password })
    const profile = await authApi.fetchCurrentUser()
    setUser(profile)
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: Boolean(user),
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
