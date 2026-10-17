import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, imgUrl, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { Spinner } from '../components/Misc'

const FLOW = ['placed', 'confirmed', 'packed', 'shipped', 'out_for_delivery', 'delivered']
const label = (s) => s.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase())

export function Orders() {
  const { t } = useApp()
  const [orders, setOrders] = useState(null)
  const [err, setErr] = useState('')
  useEffect(() => { api('/api/orders').then(setOrders).catch((e) => setErr(e.message)) }, [])
  if (err) return <div className="page"><p className="notice err">{err}</p></div>
  if (!orders) return <div className="page"><Spinner label="Loading your orders…" /></div>
  return (
    <div className="page"><h1>📦 {t('my_orders').replace('📦 ', '')}</h1>
      {!orders.length && <p className="empty">No orders yet.</p>}
      {orders.map((o) => (
        <Link key={o.id} to={`/orders/${o.id}`} className="card order">
          <div className="row between"><b>Order #{o.id}</b><span className={`pill st-${o.status}`}>{label(o.status)}</span></div>
          <div className="row">{o.items.slice(0, 4).map((i) => <img key={i.product_id} src={imgUrl(i.image)} alt={i.name} className="thumb" />)}<span className="muted">{o.items.map((i) => i.name).join(', ')}</span></div>
          <div className="row between"><span className="muted">{new Date(o.created_at).toLocaleDateString('en-IN')}</span><b>{money(o.total)}</b></div>
        </Link>
      ))}
    </div>
  )
}

export function OrderDetail() {
  const { id } = useParams()
  const { t, toast } = useApp()
  const [o, setO] = useState(null)
  const [err, setErr] = useState('')
  useEffect(() => { api(`/api/orders/${id}`).then(setO).catch((e) => setErr(e.message)) }, [id])
  if (err) return <div className="page"><p className="notice err">{err}</p></div>
  if (!o) return <div className="page"><Spinner /></div>
  const reached = new Set(o.status_history.map((h) => h.status))
  const cancel = async () => { try { setO(await api(`/api/orders/${id}/cancel`, { method: 'POST' })); toast('Order cancelled') } catch (e) { toast(e.message, 'err') } }
  return (
    <div className="page layout">
      <section>
        <h1>{t('track')} #{o.id}</h1>
        {o.status === 'cancelled' ? <p className="notice err">This order was cancelled.</p> : (
          <ol className="timeline">{FLOW.map((s) => <li key={s} className={reached.has(s) ? 'done' : ''}><span />{label(s)}{o.status_history.find((h) => h.status === s) && <small>{new Date(o.status_history.find((h) => h.status === s).at + 'Z').toLocaleString('en-IN')}</small>}</li>)}</ol>)}
        <div className="card pad">{o.items.map((i) => <div key={i.product_id} className="line"><img src={imgUrl(i.image)} alt="" /><Link className="grow" to={`/product/${i.product_id}`}>{i.name} × {i.quantity}</Link><b>{money(i.price * i.quantity)}</b></div>)}</div>
      </section>
      <aside className="card pad summary">
        <div className="row between"><span>Subtotal</span><span>{money(o.subtotal)}</span></div>
        {o.discount > 0 && <div className="row between ok"><span>Coupon {o.coupon_code}</span><span>−{money(o.discount)}</span></div>}
        <div className="row between"><span>Delivery</span><span>{o.delivery_fee ? money(o.delivery_fee) : 'Free'}</span></div>
        <div className="row between big"><b>{t('total')}</b><b>{money(o.total)}</b></div>
        <p className="muted small">Payment: {o.payment_method === 'cod' ? 'Cash on delivery' : 'Demo online'} ({o.payment_status})</p>
        <p className="small">📍 {o.address.full_name}, {o.address.line1}, {o.address.city}, {o.address.state} - {o.address.pincode}</p>
        {['placed', 'confirmed'].includes(o.status) && <button className="btn danger block" onClick={cancel}>Cancel order</button>}
      </aside>
    </div>
  )
}
