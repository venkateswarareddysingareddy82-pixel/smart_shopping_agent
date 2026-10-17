import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, imgUrl, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'
import { ProductGrid, Stars } from '../components/ProductCard'
import { Spinner } from '../components/Misc'

export default function ProductDetail() {
  const { id } = useParams()
  const nav = useNavigate()
  const { t, addToCart, toggleWish, wishIds, toggleCompare, compareIds, user, toast } = useApp()
  const { open } = useAssistant()
  const [p, setP] = useState(null)
  const [err, setErr] = useState('')
  const [img, setImg] = useState(0)
  const [qty, setQty] = useState(1)
  const [reviews, setReviews] = useState([])
  const [rv, setRv] = useState({ rating: 5, comment: '' })

  const load = () => { api(`/api/products/${id}`).then((d) => { setP(d); setImg(0) }).catch((e) => setErr(e.message)); api(`/api/reviews/product/${id}`).then(setReviews).catch(() => {}) }
  useEffect(() => { setP(null); setErr(''); load() }, [id]) // eslint-disable-line

  if (err) return <div className="page"><p className="notice err" role="alert">{err}</p></div>
  if (!p) return <div className="page"><Spinner /></div>
  const submitReview = async (e) => {
    e.preventDefault()
    try { await api(`/api/reviews/product/${id}`, { method: 'POST', body: rv }); toast('Thank you for your review!'); setRv({ rating: 5, comment: '' }); load() } catch (x) { toast(x.message, 'err') }
  }
  const buyNow = async () => {
    if (!user) { toast(t('login_first'), 'err'); nav('/login', { state: { from: `/product/${id}` } }); return }
    nav(`/checkout?buy=${p.id}&qty=${qty}`)
  }
  return (
    <div className="page">
      <div className="pd">
        <div className="gallery">
          <img className="main" src={imgUrl(p.images[img])} alt={p.name} />
          <div className="thumbs">{p.images.map((u, i) => <button key={i} className={i === img ? 'on' : ''} onClick={() => setImg(i)} aria-label={`Image ${i + 1}`}><img src={imgUrl(u)} alt="" /></button>)}</div>
        </div>
        <div className="info">
          <span className="brand">{p.brand} · {p.subcategory}</span>
          <h1>{p.name}</h1>
          <div className="row"><Stars value={p.rating} /><span className="muted">{p.review_count.toLocaleString('en-IN')} reviews</span></div>
          <div className="price big"><b>{money(p.price)}</b>{p.original_price > p.price && <><s>{money(p.original_price)}</s><span className="off">{p.discount}% off</span></>}</div>
          <p className={p.in_stock ? 'ok' : 'out'}>{p.in_stock ? (p.stock <= 5 ? `Only ${p.stock} left in stock` : 'In stock') : 'Out of stock'}</p>
          <p>{p.description}</p>
          <p className="muted">🚚 {p.delivery_information} · Sold by {p.seller}</p>
          <div className="cta-ai">
            <button className="btn lg accent" onClick={() => open({ product: p, explain: true })}>{t('explain')}</button>
            <button className="btn lg ghost" onClick={() => open({ product: p, listen: true })}>{t('ask_product')}</button>
          </div>
          <div className="row buy">
            <select value={qty} onChange={(e) => setQty(+e.target.value)} aria-label={t('qty')}>{[1, 2, 3, 4, 5].map((n) => <option key={n}>{n}</option>)}</select>
            <button className="btn lg" disabled={!p.in_stock} onClick={() => addToCart(p.id, qty)}>{t('add_to_cart')}</button>
            <button className="btn lg dark" disabled={!p.in_stock} onClick={buyNow}>{t('buy_now')}</button>
          </div>
          <div className="row">
            <button className="btn ghost" onClick={() => toggleWish(p.id)}>{wishIds.includes(p.id) ? '❤️' : '🤍'} {t('wishlist')}</button>
            <button className="btn ghost" onClick={() => toggleCompare(p.id)}>{compareIds.includes(p.id) ? '✔ ' : ''}{t('compare')}</button>
          </div>
        </div>
      </div>

      <div className="two">
        <section className="card pad"><h2>{t('details')}</h2>
          <table className="spec"><tbody>{Object.entries(p.specifications).map(([k, v]) => <tr key={k}><th>{k}</th><td>{String(v)}</td></tr>)}</tbody></table></section>
        <section className="card pad"><h2>👍 / 👎</h2>
          <ul className="good">{p.advantages.map((a) => <li key={a}>{a}</li>)}</ul>
          <ul className="bad">{p.disadvantages.map((a) => <li key={a}>{a}</li>)}</ul></section>
      </div>

      <section className="card pad"><h2>Reviews</h2>
        {reviews.length === 0 && <p className="muted">No written reviews yet.</p>}
        {reviews.map((r) => <div key={r.id} className="review"><b>{r.user_name}</b> <Stars value={r.rating} /><p>{r.comment}</p></div>)}
        {user ? (
          <form onSubmit={submitReview} className="form inline">
            <label>{t('rating')}<select value={rv.rating} onChange={(e) => setRv({ ...rv, rating: +e.target.value })}>{[5, 4, 3, 2, 1].map((n) => <option key={n} value={n}>{n} ★</option>)}</select></label>
            <input placeholder="Write your review" value={rv.comment} maxLength={500} onChange={(e) => setRv({ ...rv, comment: e.target.value })} aria-label="Review" />
            <button className="btn">Submit</button>
          </form>
        ) : <p className="muted">Log in to write a review.</p>}
      </section>

      <h2>Similar products</h2>
      <ProductGrid items={p.similar} />
    </div>
  )
}
