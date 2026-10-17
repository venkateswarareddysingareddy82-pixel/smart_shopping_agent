import { useEffect, useState } from 'react'
import { api, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { Spinner } from '../components/Misc'

const TABS = ['Dashboard', 'Products', 'Orders', 'Users', 'Reviews', 'Coupons', 'Categories']
const STATUSES = ['placed', 'confirmed', 'packed', 'shipped', 'out_for_delivery', 'delivered', 'cancelled']

function useList(path, dep) {
  const [rows, setRows] = useState(null)
  const [err, setErr] = useState('')
  const reload = () => api(path).then(setRows).catch((e) => setErr(e.message))
  useEffect(() => { setRows(null); reload() }, [path, dep]) // eslint-disable-line
  return { rows, err, reload }
}

function Dashboard() {
  const { rows: d, err } = useList('/api/admin/dashboard')
  if (err) return <p className="notice err">{err}</p>
  if (!d) return <Spinner />
  return (
    <>
      <div className="stats">{[['💰 Total sales', money(d.total_sales)], ['📦 Orders', d.total_orders], ['👥 Users', d.total_users], ['🛍️ Products', d.total_products]].map(([k, v]) => <div key={k} className="card stat"><span>{k}</span><b>{v}</b></div>)}</div>
      <div className="two">
        <section className="card pad"><h3>⚠️ Low stock</h3>{d.low_stock.map((p) => <div key={p.id} className="row between"><span>{p.name}</span><b className={p.stock <= 5 ? 'out' : ''}>{p.stock}</b></div>)}</section>
        <section className="card pad"><h3>🔥 Popular products</h3>{d.popular_products.length ? d.popular_products.map((p) => <div key={p.id} className="row between"><span>{p.name}</span><b>{p.quantity} sold</b></div>) : <p className="muted">No orders yet.</p>}</section>
      </div>
      <section className="card pad"><h3>Recent orders</h3><table className="tbl"><tbody>{d.recent_orders.map((o) => <tr key={o.id}><td>#{o.id}</td><td>{o.status}</td><td>{money(o.total)}</td><td>{new Date(o.created_at + 'Z').toLocaleString('en-IN')}</td></tr>)}</tbody></table></section>
    </>
  )
}

const blank = { name: '', category: 'smartphones', subcategory: '', brand: '', description: '', price: 1000, original_price: 1200, stock: 10, rating: 0, review_count: 0, specifications: {}, metrics: {}, features: [], advantages: [], disadvantages: [], tags: [], delivery_information: 'Free delivery in 3-5 days', seller: 'Demo Seller', search_keywords: '', is_active: true }

function Products() {
  const { toast } = useApp()
  const [v, setV] = useState(0)
  const { rows, err, reload } = useList('/api/admin/products', v)
  const cats = useList('/api/admin/categories')
  const [edit, setEdit] = useState(null)
  const [q, setQ] = useState('')
  const [json, setJson] = useState({})
  const open = (p) => { setEdit(p); setJson({ specifications: JSON.stringify(p.specifications || {}, null, 1), features: (p.features || []).join('\n'), tags: (p.tags || []).join(', ') }) }
  const save = async (e) => {
    e.preventDefault()
    try {
      const body = { ...edit, specifications: JSON.parse(json.specifications || '{}'), features: json.features.split('\n').filter(Boolean), tags: json.tags.split(',').map((x) => x.trim()).filter(Boolean),
        price: +edit.price, original_price: +edit.original_price || null, stock: +edit.stock }
      ;['id', 'discount', 'images', 'image', 'group', 'in_stock', 'created_at', 'updated_at'].forEach((k) => delete body[k])
      if (edit.id) await api(`/api/admin/products/${edit.id}`, { method: 'PUT', body }); else await api('/api/admin/products', { method: 'POST', body })
      toast('Saved'); setEdit(null); setV(v + 1)
    } catch (x) { toast(x instanceof SyntaxError ? 'Specifications must be valid JSON.' : x.message, 'err') }
  }
  const del = async (p) => { if (confirm(`Delete "${p.name}"?`)) { await api(`/api/admin/products/${p.id}`, { method: 'DELETE' }); setV(v + 1) } }
  const stock = async (p, s) => { try { await api(`/api/admin/products/${p.id}/stock`, { method: 'PATCH', body: { stock: s } }); reload() } catch (x) { toast(x.message, 'err') } }
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  if (edit) return (
    <form className="form card pad" onSubmit={save}><h3>{edit.id ? `Edit #${edit.id}` : 'Add product'}</h3>
      <div className="grid2">
        <label>Name<input required value={edit.name} onChange={(e) => setEdit({ ...edit, name: e.target.value })} /></label>
        <label>Brand<input required value={edit.brand} onChange={(e) => setEdit({ ...edit, brand: e.target.value })} /></label>
        <label>Category<select value={edit.category} onChange={(e) => setEdit({ ...edit, category: e.target.value })}>{(cats.rows || []).map((c) => <option key={c.slug} value={c.slug}>{c.name}</option>)}</select></label>
        <label>Subcategory<input value={edit.subcategory} onChange={(e) => setEdit({ ...edit, subcategory: e.target.value })} /></label>
        <label>Price ₹<input type="number" min="1" required value={edit.price} onChange={(e) => setEdit({ ...edit, price: e.target.value })} /></label>
        <label>Original price ₹<input type="number" min="1" value={edit.original_price} onChange={(e) => setEdit({ ...edit, original_price: e.target.value })} /></label>
        <label>Stock<input type="number" min="0" required value={edit.stock} onChange={(e) => setEdit({ ...edit, stock: e.target.value })} /></label>
        <label>Seller<input value={edit.seller} onChange={(e) => setEdit({ ...edit, seller: e.target.value })} /></label>
      </div>
      <label>Description<textarea value={edit.description} onChange={(e) => setEdit({ ...edit, description: e.target.value })} /></label>
      <label>Specifications (JSON, e.g. {'{"RAM":"8 GB"}'})<textarea rows={5} value={json.specifications} onChange={(e) => setJson({ ...json, specifications: e.target.value })} /></label>
      <label>Features (one per line)<textarea rows={3} value={json.features} onChange={(e) => setJson({ ...json, features: e.target.value })} /></label>
      <label>Tags (comma separated)<input value={json.tags} onChange={(e) => setJson({ ...json, tags: e.target.value })} /></label>
      <div className="row"><button className="btn">Save</button><button type="button" className="btn ghost" onClick={() => setEdit(null)}>Cancel</button></div>
    </form>
  )
  return (
    <>
      <div className="row between"><input placeholder="Filter by name…" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Filter products" /><button className="btn" onClick={() => open(blank)}>+ Add product</button></div>
      <div className="scroll-x"><table className="tbl"><thead><tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Active</th><th /></tr></thead>
        <tbody>{rows.filter((p) => p.name.toLowerCase().includes(q.toLowerCase())).map((p) => (
          <tr key={p.id} className={p.is_active ? '' : 'muted'}><td>{p.id}</td><td>{p.name}</td><td>{p.category}</td><td>{money(p.price)}</td>
            <td><input className="tiny" type="number" min="0" defaultValue={p.stock} onBlur={(e) => +e.target.value !== p.stock && stock(p, +e.target.value)} aria-label="Stock" /></td>
            <td>{p.is_active ? '✔' : '—'}</td><td><button className="link" onClick={() => open(p)}>Edit</button> <button className="link" onClick={() => del(p)}>Delete</button></td></tr>))}</tbody></table></div>
    </>
  )
}

function Orders() {
  const { toast } = useApp()
  const { rows, err, reload } = useList('/api/admin/orders')
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  const set = async (o, status) => { try { await api(`/api/admin/orders/${o.id}/status`, { method: 'PATCH', body: { status } }); toast('Status updated'); reload() } catch (x) { toast(x.message, 'err') } }
  return <div className="scroll-x"><table className="tbl"><thead><tr><th>#</th><th>Customer</th><th>Items</th><th>Total</th><th>Status</th></tr></thead><tbody>{rows.map((o) => (
    <tr key={o.id}><td>{o.id}</td><td>{o.user_name}<br /><small className="muted">{o.user_email}</small></td><td>{o.items.map((i) => `${i.name} ×${i.quantity}`).join(', ')}</td><td>{money(o.total)}</td>
      <td><select value={o.status} onChange={(e) => set(o, e.target.value)} aria-label={`Status of order ${o.id}`}>{STATUSES.map((s) => <option key={s}>{s}</option>)}</select></td></tr>))}</tbody></table></div>
}

function Users() {
  const { toast, user } = useApp()
  const { rows, err, reload } = useList('/api/admin/users')
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  const toggle = async (u) => { try { await api(`/api/admin/users/${u.id}/active`, { method: 'PATCH', body: { is_active: !u.is_active } }); reload() } catch (x) { toast(x.message, 'err') } }
  return <div className="scroll-x"><table className="tbl"><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Orders</th><th>Role</th><th>Active</th></tr></thead><tbody>{rows.map((u) => (
    <tr key={u.id}><td>{u.id}</td><td>{u.name}</td><td>{u.email}</td><td>{u.orders}</td><td>{u.is_admin ? 'Admin' : 'User'}</td><td><button className="link" disabled={u.id === user.id} onClick={() => toggle(u)}>{u.is_active ? 'Disable' : 'Enable'}</button></td></tr>))}</tbody></table></div>
}

function Reviews() {
  const { rows, err, reload } = useList('/api/admin/reviews')
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  return <div className="scroll-x"><table className="tbl"><tbody>{rows.map((r) => <tr key={r.id}><td>{r.product}</td><td>{r.user}</td><td>{r.rating}★</td><td>{r.comment}</td><td><button className="link" onClick={async () => { await api(`/api/admin/reviews/${r.id}`, { method: 'DELETE' }); reload() }}>Delete</button></td></tr>)}</tbody></table></div>
}

function Coupons() {
  const { toast } = useApp()
  const { rows, err, reload } = useList('/api/admin/coupons')
  const [c, setC] = useState({ code: '', description: '', percent: 10, max_discount: 500, min_order: 0, active: true })
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  const add = async (e) => { e.preventDefault(); try { await api('/api/admin/coupons', { method: 'POST', body: { ...c, percent: +c.percent, max_discount: +c.max_discount, min_order: +c.min_order } }); setC({ ...c, code: '' }); reload() } catch (x) { toast(x.message, 'err') } }
  return (<>
    <table className="tbl"><tbody>{rows.map((x) => <tr key={x.id}><td><b>{x.code}</b></td><td>{x.percent}% (max ₹{x.max_discount}, min ₹{x.min_order})</td><td>{x.description}</td>
      <td><button className="link" onClick={async () => { await api(`/api/admin/coupons/${x.id}`, { method: 'PUT', body: { ...x, active: !x.active } }); reload() }}>{x.active ? 'Disable' : 'Enable'}</button> <button className="link" onClick={async () => { await api(`/api/admin/coupons/${x.id}`, { method: 'DELETE' }); reload() }}>Delete</button></td></tr>)}</tbody></table>
    <form className="form card pad grid2" onSubmit={add}><input required minLength={3} placeholder="CODE" value={c.code} onChange={(e) => setC({ ...c, code: e.target.value })} /><input placeholder="Description" value={c.description} onChange={(e) => setC({ ...c, description: e.target.value })} />
      <input type="number" min="1" max="90" placeholder="% off" value={c.percent} onChange={(e) => setC({ ...c, percent: e.target.value })} /><input type="number" placeholder="Max discount ₹" value={c.max_discount} onChange={(e) => setC({ ...c, max_discount: e.target.value })} />
      <input type="number" placeholder="Min order ₹" value={c.min_order} onChange={(e) => setC({ ...c, min_order: e.target.value })} /><button className="btn">Add coupon</button></form></>)
}

function Categories() {
  const { toast } = useApp()
  const { rows, err, reload } = useList('/api/admin/categories')
  const [c, setC] = useState({ slug: '', name: '', group: 'Electronics', emoji: '🛍️' })
  if (err) return <p className="notice err">{err}</p>
  if (!rows) return <Spinner />
  const add = async (e) => { e.preventDefault(); try { await api('/api/admin/categories', { method: 'POST', body: c }); setC({ ...c, slug: '', name: '' }); reload() } catch (x) { toast(x.message, 'err') } }
  const del = async (x) => { try { await api(`/api/admin/categories/${x.id}`, { method: 'DELETE' }); reload() } catch (e) { toast(e.message, 'err') } }
  return (<>
    <table className="tbl"><tbody>{rows.map((x) => <tr key={x.id}><td>{x.emoji}</td><td>{x.name}</td><td>{x.group}</td><td className="muted">{x.slug}</td><td><button className="link" onClick={() => del(x)}>Delete</button></td></tr>)}</tbody></table>
    <form className="form card pad grid2" onSubmit={add}><input required placeholder="slug (e.g. tablets)" pattern="[a-z0-9-]+" value={c.slug} onChange={(e) => setC({ ...c, slug: e.target.value })} /><input required placeholder="Name" value={c.name} onChange={(e) => setC({ ...c, name: e.target.value })} />
      <input placeholder="Group" value={c.group} onChange={(e) => setC({ ...c, group: e.target.value })} /><input placeholder="Emoji" value={c.emoji} onChange={(e) => setC({ ...c, emoji: e.target.value })} /><button className="btn">Add category</button></form></>)
}

export default function Admin() {
  const [tab, setTab] = useState('Dashboard')
  const View = { Dashboard, Products, Orders, Users, Reviews, Coupons, Categories }[tab]
  return (
    <div className="page"><h1>🛠️ Admin</h1>
      <div className="tabs" role="tablist">{TABS.map((x) => <button key={x} role="tab" aria-selected={tab === x} className={tab === x ? 'on' : ''} onClick={() => setTab(x)}>{x}</button>)}</div>
      <View />
    </div>
  )
}
