import type { ReactNode } from 'react'
import { Package, ShieldCheck, LogOut } from 'lucide-react'
import type { User } from '../types/domain'

interface LayoutProps {
  children: ReactNode
  user?: User | null
  onLogout?: () => void
}

export function Layout({ children, user, onLogout }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-indigo-600 focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-white"
      >
        Skip to main content
      </a>

      <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-900/80 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm">
              <Package className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-base font-bold tracking-tight text-white block leading-none">
                OmniStore
              </span>
              <span className="text-xs text-slate-400">Order &amp; Fulfillment Portal</span>
            </div>
          </div>

          <nav aria-label="Primary navigation" className="flex items-center gap-3">
            {user ? (
              <>
                <div className="hidden sm:flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-1.5 text-xs">
                  <ShieldCheck className="h-4 w-4 text-emerald-400" aria-hidden="true" />
                  <span className="font-medium text-slate-200">{user.email}</span>
                  <span className="rounded bg-indigo-500/20 px-1.5 py-0.5 uppercase tracking-wider text-indigo-300">
                    {user.role}
                  </span>
                </div>
                {onLogout && (
                  <button
                    type="button"
                    onClick={onLogout}
                    aria-label="Sign out"
                    className="inline-flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-200 hover:bg-slate-700 focus-visible:outline-2 focus-visible:outline-indigo-500 transition-colors cursor-pointer"
                  >
                    <LogOut className="h-3.5 w-3.5" aria-hidden="true" />
                    <span>Sign out</span>
                  </button>
                )}
              </>
            ) : (
              <span className="text-xs text-slate-400">Zero-Trust Portal</span>
            )}
          </nav>
        </div>
      </header>

      <main id="main-content" className="flex-1 mx-auto w-full max-w-6xl px-4 sm:px-6 py-8">
        {children}
      </main>

      <footer className="border-t border-slate-800 bg-slate-900/40">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
          <p>OmniChain FullStack Roadmap — Module 03</p>
          <p>React + TypeScript Strict + Tailwind CSS v4</p>
        </div>
      </footer>
    </div>
  )
}
