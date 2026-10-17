import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api, imgUrl, money } from '../services/api'
import { useApp } from '../context/AppContext'
import { speak, voiceSupport } from '../services/voice'
import { Spinner } from '../components/Misc'

export default function Compare() {
  const { t, lang, compareIds, toggleCompare, clearCompare } = useApp()
  const [sp] = useSearchParams()
  const ids = (sp.get('ids') ? sp.get('ids').split(',').map(Number) : compareIds).filter(Boolean)
  const [data, setData] = useState(null)
  const [explain, setExplain] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const key = ids.join(',')
  useEffect(() => {
    setData(null); setExplain(''); setErr('')
    if (ids.length < 2) return
    api(`/api/compare?ids=${key}`).then(setData).catch((e) => setErr(e.message))
    // eslint-disable-next-line
  }, [key])
  const ask = async () => {
    setBusy(true)
    try { const r = await api('/api/compare/explain', { method: 'POST', body: { product_ids: ids, language: lang } }); setExplain(r.explanation); if (voiceSupport.tts) speak(r.explanation, lang) }
    catch (e) { setErr(e.message) } finally { setBusy(false) }
  }
  if (ids.length < 2) return <div className="page center"><h1>{t('compare')}</h1><p className="empty">Select 2 to 4 products using the ⚖️ checkbox on product cards.</p><Link to="/products" className="btn lg">{t('buy_products')}</Link></div>
  if (err) return <div className="page"><p className="notice err">{err}</p></div>
  if (!data) return <div className="page"><Spinner /></div>
  const best = (row) => { const nums = row.values.map((v) => parseFloat(String(v).replace(/[^\d.]/g, ''))); return nums }
  return (
    <div className="page">
      <h1>{t('compare')}</h1>
      <div className="row"><button className="btn lg accent" onClick={ask} disabled={busy}>{busy ? t('thinking') : t('explain_better')}</button><button className="btn ghost" onClick={() => { clearCompare() }}>{t('clear')}</button></div>
      {explain && <div className="notice ok big-text" role="status">🤖 {explain}</div>}
      <div className="scroll-x"><table className="cmp-table">
        <thead><tr><th />{data.products.map((p) => <th key={p.id}><img src={imgUrl(p.image)} alt="" /><Link to={`/product/${p.id}`}>{p.name}</Link><button className="link" onClick={() => toggleCompare(p.id)}>{t('remove')}</button></th>)}</tr></thead>
        <tbody>{data.table.map((row) => {
          const nums = best(row); const top = row.feature === 'Price' ? Math.min(...nums.filter(Number.isFinite)) : row.feature === 'Rating' ? Math.max(...nums.filter(Number.isFinite)) : null
          return <tr key={row.feature}><th>{row.feature}</th>{row.values.map((v, i) => <td key={i} className={top !== null && nums[i] === top ? 'win' : ''}>{v}</td>)}</tr>
        })}</tbody>
      </table></div>
      <h3>🏆</h3>
      <ul>{Object.entries(data.winners).map(([f, w]) => <li key={f}><b>{f}</b>: {w.name}{w.params && w.params.v ? ` (${w.params.v})` : ''}</li>)}</ul>
    </div>
  )
}
