import { useState } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { LANGS } from '../i18n'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'

export default function Header() {
  const { t, lang, setLang, user, logout, cartCount, wishIds, compareIds, simple, setSimple } = useApp()
  const { open } = useAssistant()
  const nav = useNavigate()
  const [q, setQ] = useState('')
  const [menu, setMenu] = useState(false)
  const submit = (e) => { e.preventDefault(); if (q.trim()) nav(`/products?q=${encodeURIComponent(q.trim())}`) }
  return (
    <header className="header">
      <div className="hwrap">
        <Link to="/" className="logo" aria-label="Smart Shopping Platform home"><span className="logo-mark">🎤</span><span>Smart<b>Shopping</b></span></Link>
        <form className="search" onSubmit={submit} role="search">
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={t('search_ph')} aria-label={t('search_ph')} />
          <button type="button" className="mic-sm" onClick={() => open({ listen: true })} aria-label={t('speak')} title={t('speak')}>🎤</button>
          <button type="submit" className="btn" aria-label="Search">🔍</button>
        </form>
        <div className="hright">
          <select className="lang" aria-label={t('select_language')} value={lang} onChange={(e) => setLang(e.target.value)}>{LANGS.map((l) => <option key={l.code} value={l.code}>🌐 {l.native}</option>)}</select>
          <button className={`btn ghost sm ${simple ? 'on' : ''}`} onClick={() => { setSimple(!simple); if (!simple) nav('/simple') }} aria-pressed={simple}>🔆 {t('simple_mode')}</button>
          <Link to="/wishlist" className="hlink" aria-label={t('wishlist')}>❤️<small>{wishIds.length || ''}</small></Link>
          {compareIds.length > 0 && <Link to={`/compare?ids=${compareIds.join(',')}`} className="hlink" aria-label={t('compare')}>⚖️<small>{compareIds.length}</small></Link>}
          <Link to="/cart" className="hlink" aria-label={t('cart')}>🛒<small>{cartCount || ''}</small></Link>
          {user ? (
            <div className="acct">
              <button className="btn ghost sm" onClick={() => setMenu(!menu)} aria-expanded={menu}>👤 {user.name.split(' ')[0]}</button>
              {menu && <div className="menu" onClick={() => setMenu(false)}>
                <Link to="/profile">{t('account')}</Link><Link to="/orders">{t('orders')}</Link>
                {user.is_admin && <Link to="/admin">Admin</Link>}
                <button onClick={async () => { await logout(); nav('/') }}>{t('logout')}</button>
              </div>}
            </div>
          ) : <Link to="/login" className="btn ghost sm">{t('login')}</Link>}
        </div>
      </div>
      <nav className="subnav" aria-label="Main">
        <NavLink to="/" end>{t('home')}</NavLink>
        <NavLink to="/products">{t('products')}</NavLink>
        <NavLink to="/orders">{t('orders')}</NavLink>
        <NavLink to="/compare">{t('compare').replace('⚖️ ', '')}</NavLink>
      </nav>
    </header>
  )
}
