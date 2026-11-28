import type { ProblemDetail } from '../types/api'
import type { TokenPair } from '../types/domain'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const STORAGE_KEY = 'omnistore_tokens'

export class ApiError extends Error {
  public readonly status: number
  public readonly problem: ProblemDetail

  constructor(problem: ProblemDetail) {
    super(problem.detail || problem.title)
    this.name = 'ApiError'
    this.status = problem.status
    this.problem = problem
  }
}

// Closure encapsulating token state and refresh lock
function createTokenStore() {
  let memoryTokens: TokenPair | null = null

  const load = (): TokenPair | null => {
    if (memoryTokens) return memoryTokens
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY)
      if (!raw) return null
      memoryTokens = JSON.parse(raw) as TokenPair
      return memoryTokens
    } catch {
      return null
    }
  }

  const save = (tokens: TokenPair | null): void => {
    memoryTokens = tokens
    if (tokens) {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(tokens))
    } else {
      sessionStorage.removeItem(STORAGE_KEY)
    }
  }

  return {
    getAccessToken: () => load()?.access_token ?? null,
    getRefreshToken: () => load()?.refresh_token ?? null,
    setTokens: save,
    clear: () => save(null),
  }
}

export const tokenStore = createTokenStore()

async function parseError(response: Response): Promise<ApiError> {
  try {
    const body = (await response.json()) as Partial<ProblemDetail>
    return new ApiError({
      type: body.type ?? 'about:blank',
      title: body.title ?? response.statusText,
      status: body.status ?? response.status,
      detail: body.detail ?? 'An unexpected error occurred.',
      instance: body.instance,
    })
  } catch {
    return new ApiError({
      type: 'about:blank',
      title: response.statusText || 'Request Failed',
      status: response.status,
      detail: `HTTP ${response.status}`,
    })
  }
}

async function tryRefreshToken(): Promise<boolean> {
  const refreshToken = tokenStore.getRefreshToken()
  if (!refreshToken) return false

  const res = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })

  if (!res.ok) {
    tokenStore.clear()
    return false
  }

  const tokens = (await res.json()) as TokenPair
  tokenStore.setTokens(tokens)
  return true
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
  retryOn401 = true,
): Promise<T> {
  const headers = new Headers(options.headers)
  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json')
  }

  const accessToken = tokenStore.getAccessToken()
  if (accessToken) {
    headers.set('Authorization', `Bearer ${accessToken}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  })

  if (response.status === 401 && retryOn401) {
    const refreshed = await tryRefreshToken()
    if (refreshed) {
      return apiRequest<T>(path, options, false)
    }
  }

  if (!response.ok) {
    throw await parseError(response)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}
