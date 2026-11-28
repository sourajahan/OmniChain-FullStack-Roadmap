import { Layout } from '../components/Layout'
import { CreateOrderForm } from '../components/CreateOrderForm'
import { OrderList } from '../components/OrderList'
import { useAuth } from '../hooks/useAuth'

export function DashboardPage() {
  const { user, logout } = useAuth()

  return (
    <Layout user={user} onLogout={logout}>
      <div className="space-y-6">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
          <h1 className="text-2xl font-bold text-white">Welcome back, {user?.full_name}</h1>
          <p className="mt-1 text-sm text-slate-400">
            Manage and track OmniStore orders in real time.
          </p>
        </div>

        <CreateOrderForm />
        <OrderList />
      </div>
    </Layout>
  )
}
