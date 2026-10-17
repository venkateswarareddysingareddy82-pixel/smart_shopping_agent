import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { useApp } from '../context/AppContext'

function useAuthForm(path, initial) {
  const { loginWith, lang } = useApp()
  const nav = useNavigate()
  const loc = useLocation()
  const [f, setF] = useState(initial)
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const submit = async (e, override) => {
    e && e.preventDefault(); setErr(''); setBusy(true)
    try { const d = await api(path, { method: 'POST', auth: false, body: override || { ...f, preferred_language: lang } }); loginWith(d); nav((loc.state && loc.state.from) || '/', { replace: true }) }
    catch (x) { setErr(x.message) } finally { setBusy(false) }
  }
  return { f, setF, err, busy, submit }
}

export function Login() {
  const { t } = useApp()
  const { f, setF, err, busy, submit } = useAuthForm('/api/auth/login', { email: '', password: '' })
  return (
    <div className="page narrow"><h1>{t('login')}</h1>
      <form className="form card pad" onSubmit={submit}>
        {err && <p className="notice err" role="alert">{err}</p>}
        <label>Email<input type="email" required autoComplete="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} /></label>
        <label>Password<input type="password" required autoComplete="current-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} /></label>
        <button className="btn lg" disabled={busy}>{busy ? '…' : t('login')}</button>
        <p className="muted small">Development demo accounts: <button type="button" className="link" onClick={() => submit(null, { email: 'user@example.com', password: 'User@12345' })}>Use demo user</button> · <button type="button" className="link" onClick={() => submit(null, { email: 'admin@example.com', password: 'Admin@12345' })}>Use demo admin</button></p>
        <p>New here? <Link to="/register">{t('register')}</Link></p>
      </form></div>
  )
}

export function Register() {
  const { t } = useApp()
  const { f, setF, err, busy, submit } = useAuthForm('/api/auth/register', { name: '', email: '', password: '', phone: '' })
  return (
    <div className="page narrow"><h1>{t('register')}</h1>
      <form className="form card pad" onSubmit={submit}>
        {err && <p className="notice err" role="alert">{err}</p>}
        <label>Name<input required minLength={2} autoComplete="name" value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} /></label>
        <label>Email<input type="email" required autoComplete="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} /></label>
        <label>Phone (optional)<input type="tel" autoComplete="tel" value={f.phone} onChange={(e) => setF({ ...f, phone: e.target.value })} /></label>
        <label>Password (8+ characters)<input type="password" required minLength={8} autoComplete="new-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} /></label>
        <button className="btn lg" disabled={busy}>{busy ? '…' : t('register')}</button>
        <p>Already registered? <Link to="/login">{t('login')}</Link></p>
      </form></div>
  )
}
