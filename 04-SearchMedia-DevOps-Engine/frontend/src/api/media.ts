export interface MediaItem {
  id: string
  title: string
  tags: string[]
  original_filename: string
  stored_filename: string
  content_type: string
  size_bytes: number
  created_at: string
}

export interface MediaSearchResponse {
  items: MediaItem[]
  total: number
  page: number
  limit: number
  pages: number
  cacheStatus: string
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8001'

export async function searchMedia(q: string, page: number, limit = 6): Promise<MediaSearchResponse> {
  const params = new URLSearchParams({ q, page: String(page), limit: String(limit) })
  const res = await fetch(`${API_BASE}/api/v1/media?${params.toString()}`)
  if (!res.ok) throw new Error('Failed to fetch media')
  const data = (await res.json()) as Omit<MediaSearchResponse, 'cacheStatus'>
  return { ...data, cacheStatus: res.headers.get('X-Cache') ?? 'BYPASS' }
}

export async function uploadMedia(title: string, tags: string, file: File): Promise<MediaItem> {
  const form = new FormData()
  form.append('title', title)
  form.append('tags', tags)
  form.append('file', file)
  const res = await fetch(`${API_BASE}/api/v1/media/upload`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = (await res.json().catch(() => ({}))) as { detail?: string }
    throw new Error(err.detail ?? 'Upload failed')
  }
  return (await res.json()) as MediaItem
}

export async function deleteMedia(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/media/${encodeURIComponent(id)}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Delete failed')
}
