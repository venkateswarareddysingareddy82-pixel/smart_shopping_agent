import { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { api, imgUrl, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { Spinner } from '../components/Misc'

export function Cart() {
  const { t, refreshCart, toast } = useApp()
  const [cart, setCart] = useState(null)
  const [err, setErr] = useState('')
  const load = () => api('/api/cart').then((c) => { setCart(c); refreshCart() }).catch((e) => setErr(e.message))
  useEffect(() => { load() }, []) // eslint-disable-line
  const upd = async (pid, quantity) => { try { setCart(await api(`/api/cart/${pid}`, { method: 'PUT', body: { quantity } })); refreshCart() } catch (e) { toast(e.message, 'err') } }
  const del = async (pid) => { setCart(await api(`/api/cart/${pid}`, { method: 'DELETE' })); refreshCart() }
  if (err) return <div className="page"><p className="notice err">{err}</p></div>
  if (!cart) return <div className="page"><Spinner /></div>
  if (!cart.items.length) return <div className="page center"><h1>🛒 {t('cart')}</h1><p className="empty">Your cart is empty.</p><Link className="btn lg" to="/products">{t('buy_products')}</Link></div>
  return (
    <div className="page layout">
      <section>
        <h1>🛒 {t('cart')} ({cart.count})</h1>
        {cart.items.map(({ product: p, quantity }) => (
          <div key={p.id} className="card line">
            <img src={imgUrl(p.image)} alt={p.name} />
            <div className="grow"><Link to={`/product/${p.id}`}><b>{p.name}</b></Link><div className="muted">{money(p.price)}</div>
              <div className="row"><button className="btn ghost sm" onClick={() => upd(p.id, Math.max(1, quantity - 1))} aria-label="Decrease">−</button><b>{quantity}</b><button className="btn ghost sm" onClick={() => upd(p.id, quantity + 1)} aria-label="Increase">+</button>
                <button className="link" onClick={() => del(p.id)}>{t('remove')}</button></div></div>
            <b>{money(p.price * quantity)}</b>
          </div>
        ))}
      </section>
      <aside className="card pad summary">
        <h3>{t('total')}</h3>
        <div className="row between"><span>Subtotal</span><span>{money(cart.subtotal)}</span></div>
        <div className="row between"><span>Delivery</span><span>{cart.delivery_fee ? money(cart.delivery_fee) : 'Free'}</span></div>
        <div className="row between big"><b>{t('total')}</b><b>{money(cart.total)}</b></div>
        <Link to="/checkout" className="btn lg block">{t('checkout')}</Link>
      </aside>
    </div>
  )
}

const empty = { full_name: '', phone: '', line1: '', line2: '', city: '', state: '', pincode: '' }

export function Checkout() {
  const { t, refreshCart, toast, user } = useApp()
  const nav = useNavigate()
  const [sp] = useSearchParams()
  const buy = sp.get('buy'); const bq = +(sp.get('qty') || 1)
  const [lines, setLines] = useState(null)
  const [addrs, setAddrs] = useState([])
  const [aid, setAid] = useState(null)
  const [newAddr, setNewAddr] = useState({ ...empty, full_name: user ? user.name : '' })
  const [coupon, setCoupon] = useState('')
  const [applied, setApplied] = useState('')
  const [coupons, setCoupons] = useState([])
  const [pay, setPay] = useState('cod')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [sum, setSum] = useState(null)

  useEffect(() => {
    (async () => {
      try {
        const a = await api('/api/users/me/addresses'); setAddrs(a); if (a[0]) setAid(a[0].id)
        setCoupons(await api('/api/coupons'))
        if (buy) { const p = await api(`/api/products/${buy}`); setLines([{ product: p, quantity: bq }]) } else { const c = await api('/api/cart'); setLines(c.items) }
      } catch (e) { setErr(e.message) }
    })()
  }, []) // eslint-disable-line
  useEffect(() => {
    if (!lines) return
    const sub = lines.reduce((s, l) => s + l.product.price * l.quantity, 0)
    if (!buy) api(`/api/cart?coupon=${applied}`).then(setSum).catch((e) => { setErr(e.message); setApplied('') })
    else setSum({ subtotal: sub, discount: 0, delivery_fee: sub >= 499 ? 0 : 40, total: sub + (sub >= 499 ? 0 : 40) })
  }, [lines, applied, buy])

  const place = async () => {
    setErr(''); setBusy(true)
    try {
      const body = { payment_method: pay, coupon_code: applied, buy_now_product_id: buy ? +buy : null, buy_now_quantity: bq }
      if (aid) body.address_id = aid; else body.address = newAddr
      const o = await api('/api/orders', { method: 'POST', body })
      refreshCart(); toast(`Order #${o.id} placed!`); nav(`/orders/${o.id}`)
    } catch (e) { setErr(e.message) } finally { setBusy(false) }
  }
  if (!lines && !err) return <div className="page"><Spinner label="Preparing checkout…" /></div>
  if (lines && !lines.length) return <div className="page"><p className="empty">Your cart is empty.</p><Link className="btn" to="/products">{t('buy_products')}</Link></div>
  const f = (k) => ({ value: newAddr[k], onChange: (e) => setNewAddr({ ...newAddr, [k]: e.target.value }), required: k !== 'line2' })
  return (
    <div className="page layout">
      <section>
        <h1>{t('checkout')}</h1>
        {err && <p className="notice err" role="alert">{err}</p>}
        <div className="card pad"><h3>1. Delivery address</h3>
          {addrs.map((a) => <label key={a.id} className="radio"><input type="radio" name="addr" checked={aid === a.id} onChange={() => setAid(a.id)} /> <span><b>{a.full_name}</b>, {a.line1}, {a.city}, {a.state} - {a.pincode} · {a.phone}</span></label>)}
          <label className="radio"><input type="radio" name="addr" checked={aid === null} onChange={() => setAid(null)} /> <b>Use a new address</b></label>
          {aid === null && <div className="form grid2">
            <input placeholder="Full name" {...f('full_name')} /><input placeholder="Phone" {...f('phone')} minLength={7} />
            <input placeholder="Address line 1" {...f('line1')} /><input placeholder="Address line 2 (optional)" {...f('line2')} />
            <input placeholder="City" {...f('city')} /><input placeholder="State" {...f('state')} /><input placeholder="PIN code" {...f('pincode')} minLength={4} /></div>}
        </div>
        <div className="card pad"><h3>2. Payment (demo)</h3>
          <label className="radio"><input type="radio" checked={pay === 'cod'} onChange={() => setPay('cod')} /> Cash on delivery</label>
          <label className="radio"><input type="radio" checked={pay === 'demo_online'} onChange={() => setPay('demo_online')} /> Demo online payment <span className="muted small">(no card details are collected — simulation only)</span></label>
        </div>
        <div className="card pad"><h3>3. Items</h3>{lines && lines.map(({ product: p, quantity }) => <div key={p.id} className="line"><img src={imgUrl(p.image)} alt="" /><span className="grow">{p.name} × {quantity}</span><b>{money(p.price * quantity)}</b></div>)}</div>
      </section>
      <aside className="card pad summary">
        {!buy && <><h3>Coupon</h3><div className="row"><input value={coupon} onChange={(e) => setCoupon(e.target.value.toUpperCase())} placeholder="Coupon code" aria-label="Coupon code" /><button className="btn ghost sm" onClick={() => { setErr(''); setApplied(coupon) }}>Apply</button></div>
          <div className="chips">{coupons.map((c) => <button key={c.code} className="chip" title={c.description} onClick={() => { setCoupon(c.code); setErr(''); setApplied(c.code) }}>{c.code}</button>)}</div></>}
        {sum && <>
          <div className="row between"><span>Subtotal</span><span>{money(sum.subtotal)}</span></div>
          {sum.discount > 0 && <div className="row between ok"><span>Coupon {sum.coupon_code}</span><span>−{money(sum.discount)}</span></div>}
          <div className="row between"><span>Delivery</span><span>{sum.delivery_fee ? money(sum.delivery_fee) : 'Free'}</span></div>
          <div className="row between big"><b>{t('total')}</b><b>{money(sum.total)}</b></div></>}
        <button className="btn lg block" disabled={busy || !sum} onClick={place}>{busy ? <Spinner label="Placing order…" /> : t('place_order')}</button>
      </aside>
    </div>
  )
}
