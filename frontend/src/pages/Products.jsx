import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../services/api'
import { useApp } from '../context/AppContext'
import { ProductGrid } from '../components/ProductCard'
import { useFetch } from './Home'

export default function Products() {
  const { t } = useApp()
  const [sp, setSp] = useSearchParams()
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [understood, setUnderstood] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  const cats = useFetch('/api/categories')
  const f = { q: sp.get('q') || '', category: sp.get('category') || '', brand: sp.getAll('brand'), min_price: sp.get('min_price') || '', max_price: sp.get('max_price') || '',
    min_rating: sp.get('min_rating') || '', in_stock: sp.get('in_stock') === '1', min_discount: sp.get('min_discount') || '', sort: sp.get('sort') || 'relevance' }
  const brands = useFetch(`/api/products/brands?category=${f.category}`, [f.category])
  const qs = sp.toString()

  useEffect(() => {
    let alive = true
    setLoading(true); setError('')
    const p = new URLSearchParams()
    for (const [k, v] of Object.entries(f)) {
      if (k === 'brand') v.forEach((b) => p.append('brand', b))
      else if (k === 'in_stock') { if (v) p.set('in_stock', 'true') }
      else if (v) p.set(k, v)
    }
    p.set('lang', localStorage.getItem('ssp_lang') || 'en'); p.set('page_size', '60')
    api(`/api/products?${p}`).then((d) => { if (alive) { setItems(d.items); setTotal(d.total); setUnderstood(d.understood) } })
      .catch((e) => alive && setError(e.message)).finally(() => alive && setLoading(false))
    return () => { alive = false }
    // eslint-disable-next-line
  }, [qs])

  const set = (k, v) => { const n = new URLSearchParams(sp); if (v === '' || v === false || v == null) n.delete(k); else n.set(k, v === true ? '1' : v); setSp(n, { replace: true }) }
  const toggleBrand = (b) => { const n = new URLSearchParams(sp); const cur = n.getAll('brand'); n.delete('brand'); (cur.includes(b) ? cur.filter((x) => x !== b) : [...cur, b]).forEach((x) => n.append('brand', x)); setSp(n, { replace: true }) }

  return (
    <div className="page layout">
      <aside className={`filters ${showFilters ? 'show' : ''}`}>
        <h3>{t('filters')} <button className="link" onClick={() => setSp({}, { replace: true })}>{t('clear')}</button></h3>
        <label>{t('categories')}
          <select value={f.category} onChange={(e) => set('category', e.target.value)}>
            <option value="">All</option>{(cats.data || []).map((c) => <option key={c.slug} value={c.slug}>{c.emoji} {c.name} ({c.count})</option>)}
          </select></label>
        <fieldset><legend>{t('price')} (₹)</legend>
          <div className="row"><input type="number" min="0" placeholder="Min" value={f.min_price} onChange={(e) => set('min_price', e.target.value)} aria-label="Minimum price" />
            <input type="number" min="0" placeholder="Max" value={f.max_price} onChange={(e) => set('max_price', e.target.value)} aria-label="Maximum price" /></div></fieldset>
        <label>{t('rating')}
          <select value={f.min_rating} onChange={(e) => set('min_rating', e.target.value)}><option value="">Any</option><option value="3">3★ & up</option><option value="4">4★ & up</option><option value="4.4">4.4★ & up</option></select></label>
        <label>{t('discount')}
          <select value={f.min_discount} onChange={(e) => set('min_discount', e.target.value)}><option value="">Any</option><option value="10">10% & above</option><option value="25">25% & above</option><option value="40">40% & above</option></select></label>
        <label className="check"><input type="checkbox" checked={f.in_stock} onChange={(e) => set('in_stock', e.target.checked)} /> {t('in_stock')}</label>
        <fieldset><legend>{t('brand')}</legend>
          <div className="brandlist">{(brands.data || []).map((b) => <label key={b} className="check"><input type="checkbox" checked={f.brand.includes(b)} onChange={() => toggleBrand(b)} /> {b}</label>)}</div></fieldset>
      </aside>
      <section>
        <div className="toolbar">
          <button className="btn ghost sm only-mobile" onClick={() => setShowFilters(!showFilters)}>☰ {t('filters')}</button>
          <div><b>{loading ? '…' : total}</b> results{f.q && <> for “{f.q}”</>}</div>
          <label className="row">{t('sort')}:&nbsp;
            <select value={f.sort} onChange={(e) => set('sort', e.target.value)}>
              <option value="relevance">Relevance</option><option value="price_asc">Price: low to high</option><option value="price_desc">Price: high to low</option>
              <option value="rating">Rating</option><option value="discount">Discount</option><option value="popular">Most reviewed</option><option value="newest">Newest</option>
            </select></label>
        </div>
        {understood && (understood.category || understood.max_price || (understood.features || []).length > 0) && (
          <p className="notice ok">🤖 We understood: {[understood.category && `category: ${understood.category}`, understood.max_price && `budget up to ₹${understood.max_price.toLocaleString('en-IN')}`, (understood.features || []).length > 0 && `needs: ${understood.features.join(', ')}`].filter(Boolean).join(' · ')}</p>
        )}
        <ProductGrid items={items} loading={loading} error={error} />
      </section>
    </div>
  )
}
