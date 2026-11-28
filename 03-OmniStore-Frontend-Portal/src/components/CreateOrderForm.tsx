import { useState } from 'react'
import type { FormEvent } from 'react'
import { Plus, Trash2, ShoppingBag, AlertCircle } from 'lucide-react'
import { useCreateOrderMutation } from '../hooks/useOrders'
import { ApiError } from '../api/client'
import type { CreateOrderItemInput } from '../types/domain'

const EMPTY_ITEM: CreateOrderItemInput = {
  product_sku: '',
  product_name: '',
  quantity: 1,
  unit_price: 0,
}

export function CreateOrderForm() {
  const [items, setItems] = useState<CreateOrderItemInput[]>([{ ...EMPTY_ITEM }])
  const mutation = useCreateOrderMutation()

  const totalAmount = items.reduce((sum, item) => sum + item.quantity * item.unit_price, 0)

  const updateItem = <K extends keyof CreateOrderItemInput>(
    index: number,
    field: K,
    value: CreateOrderItemInput[K],
  ) => {
    setItems((prev) =>
      prev.map((item, idx) => (idx === index ? { ...item, [field]: value } : item)),
    )
  }

  const addItem = () => setItems((prev) => [...prev, { ...EMPTY_ITEM }])

  const removeItem = (index: number) => {
    setItems((prev) => (prev.length > 1 ? prev.filter((_, idx) => idx !== index) : prev))
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    await mutation.mutateAsync({ items })
    setItems([{ ...EMPTY_ITEM }])
  }

  const errorMessage =
    mutation.error instanceof ApiError
      ? mutation.error.problem.detail
      : mutation.error
        ? 'Failed to create order.'
        : null

  return (
    <section
      aria-labelledby="create-order-heading"
      className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6"
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <ShoppingBag className="h-5 w-5 text-indigo-400" aria-hidden="true" />
          <h2 id="create-order-heading" className="text-lg font-semibold text-white">
            Create New Order
          </h2>
        </div>
        <span className="text-sm font-medium text-emerald-400">
          Total: ${totalAmount.toFixed(2)}
        </span>
      </div>

      {errorMessage && (
        <div
          role="alert"
          className="mt-4 flex items-center gap-2 rounded-lg border border-rose-500/40 bg-rose-500/10 p-3 text-sm text-rose-200"
        >
          <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" aria-hidden="true" />
          <span>{errorMessage}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-4 space-y-3">
        {items.map((item, index) => (
          <div
            key={index}
            className="grid grid-cols-1 sm:grid-cols-12 gap-2.5 items-end rounded-xl border border-slate-800 bg-slate-950/60 p-3"
          >
            <div className="sm:col-span-3">
              <label htmlFor={`sku-${index}`} className="block text-xs text-slate-400">
                SKU
              </label>
              <input
                id={`sku-${index}`}
                type="text"
                required
                placeholder="SKU-001"
                value={item.product_sku}
                onChange={(e) => updateItem(index, 'product_sku', e.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-900 px-2.5 py-1.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-4">
              <label htmlFor={`name-${index}`} className="block text-xs text-slate-400">
                Product Name
              </label>
              <input
                id={`name-${index}`}
                type="text"
                required
                placeholder="Mechanical Keyboard"
                value={item.product_name}
                onChange={(e) => updateItem(index, 'product_name', e.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-900 px-2.5 py-1.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-2">
              <label htmlFor={`qty-${index}`} className="block text-xs text-slate-400">
                Qty
              </label>
              <input
                id={`qty-${index}`}
                type="number"
                min={1}
                required
                value={item.quantity}
                onChange={(e) => updateItem(index, 'quantity', Math.max(1, Number(e.target.value)))}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-900 px-2.5 py-1.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-2">
              <label htmlFor={`price-${index}`} className="block text-xs text-slate-400">
                Unit Price ($)
              </label>
              <input
                id={`price-${index}`}
                type="number"
                min={0.01}
                step="0.01"
                required
                value={item.unit_price || ''}
                onChange={(e) => updateItem(index, 'unit_price', Math.max(0, Number(e.target.value)))}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-900 px-2.5 py-1.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-1 flex justify-end">
              <button
                type="button"
                onClick={() => removeItem(index)}
                disabled={items.length === 1}
                aria-label={`Remove item ${index + 1}`}
                className="rounded-lg border border-slate-700 p-2 text-slate-400 hover:text-rose-400 disabled:opacity-40 cursor-pointer"
              >
                <Trash2 className="h-4 w-4" aria-hidden="true" />
              </button>
            </div>
          </div>
        ))}

        <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
          <button
            type="button"
            onClick={addItem}
            className="inline-flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-medium text-slate-200 hover:bg-slate-700 cursor-pointer"
          >
            <Plus className="h-4 w-4" aria-hidden="true" />
            Add item
          </button>

          <button
            type="submit"
            disabled={mutation.isPending}
            className="rounded-lg bg-indigo-600 px-5 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-colors cursor-pointer"
          >
            {mutation.isPending ? 'Submitting...' : 'Place Order'}
          </button>
        </div>
      </form>
    </section>
  )
}
