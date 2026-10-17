import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { api, getToken, setToken } from '../services/api'
import { translate } from '../i18n'

const Ctx = createContext(null)
export const useApp = () => useContext(Ctx)

const readJSON = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d } catch { return d } }

export function AppProvider({ children }) {
  const [lang, setLangState] = useState(localStorage.getItem('ssp_lang') || 'en')
  const [langChosen, setLangChosen] = useState(!!localStorage.getItem('ssp_lang'))
  const [simple, setSimpleState] = useState(localStorage.getItem('ssp_simple') === '1')
  const [user, setUser] = useState(null)
  const [authReady, setAuthReady] = useState(false)
  const [cartCount, setCartCount] = useState(0)
  const [wishIds, setWishIds] = useState([])
  const [compareIds, setCompareIds] = useState(readJSON('ssp_compare', []))
  const [toasts, setToasts] = useState([])

  const t = useCallback((k) => translate(lang, k), [lang])
  const setLang = (l) => { setLangState(l); setLangChosen(true); localStorage.setItem('ssp_lang', l); document.documentElement.lang = l }
  const setSimple = (v) => { setSimpleState(v); localStorage.setItem('ssp_simple', v ? '1' : '0') }

  const toast = useCallback((message, kind = 'ok') => {
    const id = Math.random()
    setToasts((x) => [...x, { id, message, kind }])
    setTimeout(() => setToasts((x) => x.filter((y) => y.id !== id)), 4000)
  }, [])

  const refreshCart = useCallback(async () => {
    if (!getToken()) { setCartCount(0); setWishIds([]); return }
    try {
      const [c, w] = await Promise.all([api('/api/cart'), api('/api/wishlist')])
      setCartCount(c.count); setWishIds(w.map((p) => p.id))
    } catch { /* ignore */ }
  }, [])

  useEffect(() => {
    document.documentElement.lang = lang
    if (!getToken()) { setAuthReady(true); return }
    api('/api/auth/me').then((u) => { setUser(u); refreshCart() }).catch(() => setToken(null)).finally(() => setAuthReady(true))
    // eslint-disable-next-line
  }, [])

  const loginWith = (data) => { setToken(data.token); setUser(data.user); if (!localStorage.getItem('ssp_lang') && data.user.preferred_language) setLang(data.user.preferred_language); setTimeout(refreshCart, 0) }
  const logout = async () => { try { await api('/api/auth/logout', { method: 'POST' }) } catch { /* ignore */ } setToken(null); setUser(null); setCartCount(0); setWishIds([]) }

  const toggleCompare = (id) => {
    setCompareIds((cur) => {
      let next = cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id]
      if (next.length > 4) { toast('You can compare up to 4 products.', 'err'); next = cur }
      localStorage.setItem('ssp_compare', JSON.stringify(next))
      return next
    })
  }
  const clearCompare = () => { setCompareIds([]); localStorage.setItem('ssp_compare', '[]') }

  const addToCart = async (id, qty = 1) => {
    if (!getToken()) { toast(t('login_first'), 'err'); return false }
    try { const c = await api('/api/cart', { method: 'POST', body: { product_id: id, quantity: qty } }); setCartCount(c.count); toast(t('added_cart')); return true }
    catch (e) { toast(e.message, 'err'); return false }
  }
  const toggleWish = async (id) => {
    if (!getToken()) { toast(t('login_first'), 'err'); return }
    try {
      if (wishIds.includes(id)) { await api(`/api/wishlist/${id}`, { method: 'DELETE' }); setWishIds((w) => w.filter((x) => x !== id)) }
      else { await api(`/api/wishlist/${id}`, { method: 'POST' }); setWishIds((w) => [...w, id]); toast(t('added_wish')) }
    } catch (e) { toast(e.message, 'err') }
  }

  const value = useMemo(() => ({ lang, setLang, langChosen, simple, setSimple, t, user, authReady, loginWith, logout, cartCount, refreshCart, wishIds, toggleWish,
    compareIds, toggleCompare, clearCompare, addToCart, toast, toasts }), [lang, langChosen, simple, user, authReady, cartCount, wishIds, compareIds, toasts]) // eslint-disable-line
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}
