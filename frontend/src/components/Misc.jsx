import { Link, Navigate, useLocation } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'

export function Toasts() {
  const { toasts } = useApp()
  return <div className="toasts" role="status" aria-live="polite">{toasts.map((x) => <div key={x.id} className={`toast ${x.kind}`}>{x.message}</div>)}</div>
}

export function Footer() {
  return <footer className="footer"><p><b>Smart Shopping Platform</b> — demo project. All products, brands and prices are fictional demo data.</p><p className="muted small">No real payments are processed. Voice recognition uses your browser (Chrome / Edge recommended).</p></footer>
}

export function Fab() {
  const { t } = useApp()
  const { isOpen, open } = useAssistant()
  if (isOpen) return null
  return <button className="fab" onClick={() => open({})} aria-label={t('ask_assistant')}><span>🤖</span><span className="fab-t">{t('ask_assistant').replace('🤖 ', '')}</span></button>
}

export function Protected({ children, admin }) {
  const { user, authReady } = useApp()
  const loc = useLocation()
  if (!authReady) return <div className="page"><p className="muted">Loading…</p></div>
  if (!user) return <Navigate to="/login" state={{ from: loc.pathname + loc.search }} replace />
  if (admin && !user.is_admin) return <div className="page"><p className="notice err">Only administrators can open this page.</p><Link to="/">Home</Link></div>
  return children
}

export function Spinner({ label = 'Loading…' }) { return <div className="spinner-wrap" role="status"><span className="spinner" /> {label}</div> }
