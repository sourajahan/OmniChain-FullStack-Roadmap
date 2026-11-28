export interface ProblemDetail {
  type: string
  title: string
  status: number
  detail: string
  instance?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}

export type AsyncStatus = 'idle' | 'loading' | 'success' | 'error'

export interface ApiResult<T> {
  data: T | null
  error: ProblemDetail | null
  status: AsyncStatus
}
