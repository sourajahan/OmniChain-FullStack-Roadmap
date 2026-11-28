import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { SearchPage } from './pages/SearchPage'
import { UploadPage } from './pages/UploadPage'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 10_000 } },
})

export function AppRoutes() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/70">
        <div className="mx-auto max-w-4xl px-4 h-16 flex items-center justify-between">
          <Link to="/" className="font-bold text-white">SearchMedia Engine</Link>
          <nav aria-label="Main navigation" className="flex gap-4 text-sm">
            <Link to="/" className="text-slate-300 hover:text-white">Search</Link>
            <Link to="/upload" className="text-indigo-400 hover:text-indigo-300 font-medium">Upload</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-4xl px-4 py-8">
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </QueryClientProvider>
  )
}
