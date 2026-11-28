import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Search, Trash2, Database } from 'lucide-react'
import { deleteMedia, searchMedia } from '../api/media'

export function SearchPage() {
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(1)
  const queryClient = useQueryClient()

  const { data, isLoading, isError } = useQuery({
    queryKey: ['media', query, page],
    queryFn: () => searchMedia(query, page, 6),
  })

  const remove = useMutation({
    mutationFn: (id: string) => deleteMedia(id),
    onSuccess: () => void queryClient.invalidateQueries({ queryKey: ['media'] }),
  })

  return (
    <section className="space-y-5">
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" aria-hidden="true" />
          <input
            aria-label="Search media"
            type="search"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value)
              setPage(1)
            }}
            placeholder="Search by title, tags, or filename..."
            className="w-full rounded-xl border border-slate-700 bg-slate-900 pl-9 pr-3 py-2 text-sm text-white focus:border-indigo-500 focus:outline-none"
          />
        </div>
        {data && (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs font-mono text-indigo-300">
            <Database className="h-3.5 w-3.5" aria-hidden="true" />
            X-Cache: {data.cacheStatus}
          </span>
        )}
      </div>

      {isLoading && <p role="status" className="text-sm text-slate-400">Loading media...</p>}
      {isError && <p role="alert" className="text-sm text-rose-400">Could not load media items.</p>}

      {data && data.items.length === 0 && (
        <p className="rounded-xl border border-dashed border-slate-800 py-10 text-center text-sm text-slate-400">
          No media found.
        </p>
      )}

      {data && data.items.length > 0 && (
        <>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.items.map((item) => (
              <li key={item.id} className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 flex justify-between gap-3">
                <div className="space-y-1">
                  <h3 className="font-semibold text-white">{item.title}</h3>
                  <p className="text-xs text-slate-400">{item.original_filename} · {(item.size_bytes / 1024).toFixed(1)} KB</p>
                  <div className="flex flex-wrap gap-1 pt-1">
                    {item.tags.map((tag) => (
                      <span key={tag} className="rounded bg-slate-800 px-2 py-0.5 text-xs text-indigo-300">#{tag}</span>
                    ))}
                  </div>
                </div>
                <button
                  type="button"
                  aria-label={`Delete ${item.title}`}
                  onClick={() => remove.mutate(item.id)}
                  className="self-start rounded-lg border border-slate-700 p-2 text-slate-400 hover:text-rose-400 cursor-pointer"
                >
                  <Trash2 className="h-4 w-4" aria-hidden="true" />
                </button>
              </li>
            ))}
          </ul>

          <div className="flex items-center justify-between pt-2 text-xs text-slate-400">
            <span>Page {data.page} of {data.pages} ({data.total} total)</span>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="rounded-lg border border-slate-700 px-3 py-1.5 text-white disabled:opacity-40 cursor-pointer"
              >
                Prev
              </button>
              <button
                type="button"
                disabled={page >= data.pages}
                onClick={() => setPage((p) => p + 1)}
                className="rounded-lg border border-slate-700 px-3 py-1.5 text-white disabled:opacity-40 cursor-pointer"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </section>
  )
}
