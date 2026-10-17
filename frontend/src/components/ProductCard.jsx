import { Link } from 'react-router-dom'
import { imgUrl, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'

export const Stars = ({ value }) => <span className="stars" aria-label={`${value} out of 5`}>★ {Number(value).toFixed(1)}</span>

export default function ProductCard({ p }) {
  const { t, addToCart, toggleWish, wishIds, compareIds, toggleCompare, simple } = useApp()
  const { open } = useAssistant()
  const wished = wishIds.includes(p.id)
  const inCompare = compareIds.includes(p.id)
  return (
    <article className="card product">
      <button className={`wish ${wished ? 'on' : ''}`} onClick={() => toggleWish(p.id)} aria-label={t('wishlist')} aria-pressed={wished}>{wished ? '❤️' : '🤍'}</button>
      {p.discount >= 10 && <span className="badge">{p.discount}% off</span>}
      <Link to={`/product/${p.id}`} className="pimg"><img src={imgUrl(p.image)} alt={p.name} loading="lazy" /></Link>
      <div className="pbody">
        <span className="brand">{p.brand}</span>
        <Link to={`/product/${p.id}`} className="pname">{p.name}</Link>
        <div className="row"><Stars value={p.rating} /><span className="muted small">({p.review_count.toLocaleString('en-IN')})</span></div>
        <div className="price"><b>{money(p.price)}</b>{p.original_price > p.price && <s>{money(p.original_price)}</s>}</div>
        {!p.in_stock && <div className="out">Out of stock</div>}
        {p.why && p.why[0] && <div className="why">{p.why[0]}</div>}
        <div className="actions">
          <button className="btn" disabled={!p.in_stock} onClick={() => addToCart(p.id)}>{t('add_to_cart')}</button>
          <button className="btn ghost" onClick={() => open({ product: p, explain: true })}>{t('explain')}</button>
          {!simple && <label className="cmp"><input type="checkbox" checked={inCompare} onChange={() => toggleCompare(p.id)} /> ⚖️ {t('compare').replace('⚖️ ', '')}</label>}
          {simple && <button className="btn ghost" onClick={() => toggleCompare(p.id)}>{inCompare ? '✔ ' : ''}{t('compare')}</button>}
        </div>
      </div>
    </article>
  )
}

export function Skeletons({ n = 8 }) {
  return <div className="grid">{Array.from({ length: n }).map((_, i) => <div key={i} className="card skel"><div className="sk-img" /><div className="sk-line" /><div className="sk-line short" /></div>)}</div>
}

export function ProductGrid({ items, loading, error }) {
  const { t } = useApp()
  if (loading) return <Skeletons />
  if (error) return <p className="notice err" role="alert">{error}</p>
  if (!items.length) return <p className="empty">🔍 {t('no_results')}</p>
  return <div className="grid">{items.map((p) => <ProductCard key={p.id} p={p} />)}</div>
}
