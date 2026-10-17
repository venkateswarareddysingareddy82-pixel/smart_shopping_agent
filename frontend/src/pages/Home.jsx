import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { SAMPLES, LANGS } from '../i18n'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'
import { ProductGrid } from '../components/ProductCard'

export function useFetch(path, deps = []) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  useEffect(() => {
    let alive = true
    setLoading(true); setError('')
    api(path).then((d) => alive && setData(d)).catch((e) => alive && setError(e.message)).finally(() => alive && setLoading(false))
    return () => { alive = false }
    // eslint-disable-next-line
  }, [path, ...deps])
  return { data, loading, error }
}

export default function Home() {
  const { t, lang, setLang, user } = useApp()
  const { open } = useAssistant()
  const cats = useFetch('/api/categories')
  const rec = useFetch('/api/recommendations?limit=8', [user && user.id])
  const deals = useFetch('/api/products?sort=discount&min_discount=30&in_stock=true&page_size=4')
  const popular = useFetch('/api/products?sort=popular&page_size=8')
  const groups = cats.data ? [...new Set(cats.data.map((c) => c.group))] : []
  return (
    <>
      <section className="hero">
        <div className="hwrap hero-grid">
          <div>
            <h1>{t('hero_title')}</h1>
            <p className="lead">{t('hero_sub')}</p>
            <ul className="steps">{[1, 2, 3, 4].map((n, i) => <li key={n}><span>{['🎤', '🤖', '🛍️', '🔊'][i]}</span>{t(`hero_${n}`)}</li>)}</ul>
          </div>
          <div className="mic-stage">
            <button className="mic-big" onClick={() => open({ listen: true })} aria-label={t('speak_search')}><span>🎤</span></button>
            <p className="mic-cta">{t('tap_speak')}</p>
            <p className="sample">“{SAMPLES[lang]}”</p>
            <div className="chips center">{LANGS.map((l) => <button key={l.code} className={`chip ${l.code === lang ? 'on' : ''}`} onClick={() => setLang(l.code)}>{l.native}</button>)}</div>
          </div>
        </div>
      </section>

      <div className="page">
        <h2>{t('categories')}</h2>
        {cats.loading ? <p className="muted">…</p> : groups.map((g) => (
          <div key={g} className="cat-group"><h3>{g}</h3>
            <div className="cat-row">{cats.data.filter((c) => c.group === g).map((c) => (
              <Link key={c.slug} to={`/products?category=${c.slug}`} className="cat"><span>{c.emoji}</span>{c.name}</Link>
            ))}</div>
          </div>
        ))}

        <section className="ai-band">
          <div><h2>🤖 {t('ask_assistant').replace('🤖 ', '')}</h2><p>“I don't know which refrigerator is good. Suggest one for a family of four.”</p></div>
          <button className="btn lg" onClick={() => open({ listen: true })}>{t('speak_search')}</button>
          <button className="btn ghost lg" onClick={() => open({ prompt: 'I don\'t know what to buy. Ask me questions.' })}>💬 Help me choose</button>
        </section>

        <h2>✨ {t('recommended')}</h2>
        <ProductGrid items={(rec.data && rec.data.items) || []} loading={rec.loading} error={rec.error} />
        <h2>🏷️ {t('deals')}</h2>
        <ProductGrid items={(deals.data && deals.data.items) || []} loading={deals.loading} error={deals.error} />
        <h2>🔥 {t('popular')}</h2>
        <ProductGrid items={(popular.data && popular.data.items) || []} loading={popular.loading} error={popular.error} />
      </div>
    </>
  )
}
