import { useState } from 'react'
import type { FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { UploadCloud, AlertCircle } from 'lucide-react'
import { uploadMedia } from '../api/media'

const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/webp', 'application/pdf', 'text/plain']
const MAX_BYTES = 5 * 1024 * 1024

export function UploadPage() {
  const [title, setTitle] = useState('')
  const [tags, setTags] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [validationError, setValidationError] = useState<string | null>(null)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: () => uploadMedia(title.trim(), tags.trim(), file as File),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['media'] })
      navigate('/')
    },
  })

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setValidationError(null)
    if (title.trim().length < 2) {
      setValidationError('Title must be at least 2 characters.')
      return
    }
    if (!file) {
      setValidationError('Please select a file to upload.')
      return
    }
    if (!ALLOWED_TYPES.includes(file.type)) {
      setValidationError('Unsupported file type. Use PNG, JPEG, WEBP, PDF, or TXT.')
      return
    }
    if (file.size > MAX_BYTES) {
      setValidationError('File exceeds the 5MB limit.')
      return
    }
    mutation.mutate()
  }

  const errorText = validationError ?? (mutation.error instanceof Error ? mutation.error.message : null)

  return (
    <section className="mx-auto max-w-lg rounded-2xl border border-slate-800 bg-slate-900/70 p-6 space-y-4">
      <div className="flex items-center gap-2">
        <UploadCloud className="h-5 w-5 text-indigo-400" aria-hidden="true" />
        <h2 className="text-lg font-semibold text-white">Upload Media</h2>
      </div>

      {errorText && (
        <div role="alert" className="flex items-center gap-2 rounded-lg border border-rose-500/40 bg-rose-500/10 p-3 text-sm text-rose-200">
          <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" aria-hidden="true" />
          <span>{errorText}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        <div>
          <label htmlFor="media-title" className="block text-xs text-slate-300">Title</label>
          <input
            id="media-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Architecture Diagram"
            className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white"
          />
        </div>
        <div>
          <label htmlFor="media-tags" className="block text-xs text-slate-300">Tags (comma separated)</label>
          <input
            id="media-tags"
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="devops, redis, docker"
            className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white"
          />
        </div>
        <div>
          <label htmlFor="media-file" className="block text-xs text-slate-300">File (PNG, JPG, WEBP, PDF, TXT — max 5MB)</label>
          <input
            id="media-file"
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="mt-1 block w-full text-xs text-slate-300"
          />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending}
          className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 cursor-pointer"
        >
          {mutation.isPending ? 'Uploading...' : 'Upload Asset'}
        </button>
      </form>
    </section>
  )
}
