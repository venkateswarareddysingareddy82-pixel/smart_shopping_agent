import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { useApp } from '../context/AppContext'

const empty = { full_name: '', phone: '', line1: '', line2: '', city: '', state: '', pincode: '', is_default: false }

export default function Profile() {
  const { user, toast, lang } = useApp()
  const [name, setName] = useState(user.name)
  const [phone, setPhone] = useState(user.phone || '')
  const [addrs, setAddrs] = useState([])
  const [notes, setNotes] = useState([])
  const [a, setA] = useState(empty)
  const load = () => { api('/api/users/me/addresses').then(setAddrs).catch(() => {}); api('/api/users/me/notifications').then(setNotes).catch(() => {}) }
  useEffect(() => { load(); api('/api/users/me/notifications/read', { method: 'POST' }).catch(() => {}) }, [])
  const save = async (e) => { e.preventDefault(); try { await api('/api/users/me', { method: 'PUT', body: { name, phone, preferred_language: lang } }); toast('Profile saved') } catch (x) { toast(x.message, 'err') } }
  const addAddr = async (e) => { e.preventDefault(); try { await api('/api/users/me/addresses', { method: 'POST', body: a }); setA(empty); load(); toast('Address added') } catch (x) { toast(x.message, 'err') } }
  const del = async (id) => { await api(`/api/users/me/addresses/${id}`, { method: 'DELETE' }); load() }
  const f = (k) => ({ value: a[k], onChange: (e) => setA({ ...a, [k]: e.target.value }), required: k !== 'line2' })
  return (
    <div className="page two">
      <section><h1>👤 Profile</h1>
        <form className="form card pad" onSubmit={save}><label>Name<input value={name} minLength={2} onChange={(e) => setName(e.target.value)} /></label>
          <label>Email<input value={user.email} disabled /></label><label>Phone<input value={phone} onChange={(e) => setPhone(e.target.value)} /></label><button className="btn">Save</button></form>
        <h2>Addresses</h2>
        {addrs.map((x) => <div key={x.id} className="card pad row between"><span>{x.full_name}, {x.line1}, {x.city}, {x.state} - {x.pincode}{x.is_default && ' ⭐'}</span><button className="link" onClick={() => del(x.id)}>Delete</button></div>)}
        <form className="form card pad grid2" onSubmit={addAddr}>
          <input placeholder="Full name" {...f('full_name')} /><input placeholder="Phone" {...f('phone')} /><input placeholder="Address line 1" {...f('line1')} /><input placeholder="Address line 2" {...f('line2')} />
          <input placeholder="City" {...f('city')} /><input placeholder="State" {...f('state')} /><input placeholder="PIN code" {...f('pincode')} /><button className="btn">Add address</button></form>
      </section>
      <section><h2>🔔 Notifications</h2>{!notes.length && <p className="muted">Nothing yet.</p>}
        {notes.map((n) => <div key={n.id} className="card pad"><b>{n.title}</b><p className="muted small">{n.message} · {new Date(n.created_at + 'Z').toLocaleString('en-IN')}</p></div>)}</section>
    </div>
  )
}
