import { useState } from 'react'
import { RefreshCw, AlertCircle, PackageOpen } from 'lucide-react'
import { useOrdersQuery, useUpdateOrderStatusMutation } from '../hooks/useOrders'
import { useAuth } from '../hooks/useAuth'
import type { OrderStatus } from '../types/domain'

const STATUS_OPTIONS: Array<OrderStatus | 'all'> = [
  'all',
  'pending',
  'confirmed',
  'shipped',
  'delivered',
  'cancelled',
]

const NEXT_STATUS: Partial<Record<OrderStatus, OrderStatus>> = {
  pending: 'confirmed',
  confirmed: 'shipped',
  shipped: 'delivered',
}

const STATUS_BADGE: Record<OrderStatus, string> = {
  pending: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  confirmed: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
  shipped: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
  delivered: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  cancelled: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
}

export function OrderList() {
  const { user } = useAuth()
  const [statusFilter, setStatusFilter] = useState<OrderStatus | 'all'>('all')
  const { data, isLoading, isError, error, refetch } = useOrdersQuery(statusFilter)
  const updateStatus = useUpdateOrderStatusMutation()

  const canManageStatus = user?.role === 'warehouse' || user?.role === 'admin'

  return (
    <section
      aria-labelledby="orders-heading"
      className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 space-y-4"
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 id="orders-heading" className="text-lg font-semibold text-white">
            Orders
          </h2>
          <p className="text-xs text-slate-400">
            {data ? `Showing ${data.items.length} of ${data.total} orders` : 'Live order feed'}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="status-filter" className="text-xs text-slate-400">
            Filter:
          </label>
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as OrderStatus | 'all')}
            className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs text-white focus:border-indigo-500 focus:outline-none"
          >
            {STATUS_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt.toUpperCase()}
              </option>
            ))}
          </select>
        </div>
      </div>

      {isLoading && (
        <div role="status" aria-label="Loading orders" className="space-y-3">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-20 animate-pulse rounded-xl bg-slate-800/60" />
          ))}
        </div>
      )}

      {isError && (
        <div
          role="alert"
          className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-200"
        >
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" aria-hidden="true" />
            <span>{error instanceof Error ? error.message : 'Could not load orders.'}</span>
          </div>
          <button
            type="button"
            onClick={() => void refetch()}
            className="inline-flex items-center gap-1.5 rounded-lg border border-rose-400/40 px-3 py-1.5 text-xs font-medium text-rose-100 hover:bg-rose-500/20 cursor-pointer"
          >
            <RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />
            Retry
          </button>
        </div>
      )}

      {!isLoading && !isError && data && data.items.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-800 py-12 text-center">
          <PackageOpen className="h-8 w-8 text-slate-600" aria-hidden="true" />
          <p className="mt-2 text-sm text-slate-400">No orders found for this filter.</p>
        </div>
      )}

      {!isLoading && !isError && data && data.items.length > 0 && (
        <ul className="space-y-3">
          {data.items.map((order) => {
            const nextStatus = NEXT_STATUS[order.status]
            return (
              <li
                key={order.id}
                className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono text-xs text-slate-400">#{order.id.slice(0, 8)}</span>
                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-medium uppercase ${STATUS_BADGE[order.status]}`}
                    >
                      {order.status}
                    </span>
                    <span className="text-sm font-semibold text-white">
                      ${Number(order.total_amount).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">
                    {order.items.map((i) => `${i.quantity}× ${i.product_name}`).join(', ')}
                  </p>
                </div>

                {canManageStatus && nextStatus && (
                  <button
                    type="button"
                    disabled={updateStatus.isPending}
                    onClick={() => updateStatus.mutate({ orderId: order.id, status: nextStatus })}
                    className="rounded-lg border border-indigo-500/40 bg-indigo-500/10 px-3 py-1.5 text-xs font-medium text-indigo-300 hover:bg-indigo-500/20 disabled:opacity-50 cursor-pointer"
                  >
                    Mark as {nextStatus}
                  </button>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
