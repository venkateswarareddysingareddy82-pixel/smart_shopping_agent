import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, imgUrl, money } from '../services/api'
import { listen, speak, stopSpeaking, voiceSupport, hasVoiceFor } from '../services/voice'
import { LANGS } from '../i18n'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'

function MiniProduct({ p }) {
  const { addToCart, t } = useApp()
  return (
    <div className="mini">
      <Link to={`/product/${p.id}`}><img src={imgUrl(p.image)} alt={p.name} loading="lazy" /></Link>
      <div className="mini-body">
        <Link to={`/product/${p.id}`} className="mini-name">{p.name}</Link>
        <div><b>{money(p.price)}</b> {p.discount > 0 && <span className="off">{p.discount}% off</span>} <span className="muted">★ {p.rating}</span></div>
        {p.why && p.why[0] && <div className="why">{p.why[0]}</div>}
        <button className="btn sm" onClick={() => addToCart(p.id)}>{t('add_to_cart')}</button>
      </div>
    </div>
  )
}

export default function AssistantPanel() {
  const { lang, setLang, langChosen, t, toast } = useApp()
  const { isOpen, close, request } = useAssistant()
  const [messages, setMessages] = useState([])
  const [state, setState] = useState({})
  const [input, setInput] = useState('')
  const [phase, setPhase] = useState('idle') // idle | listening | thinking | speaking
  const [interim, setInterim] = useState('')
  const [ttsOn, setTtsOn] = useState(true)
  const [pickLang, setPickLang] = useState(false)
  const [product, setProduct] = useState(null)
  const [notice, setNotice] = useState('')
  const recRef = useRef(null)
  const endRef = useRef(null)
  const stateRef = useRef({})
  stateRef.current = { messages, state, product, lang, ttsOn }

  useEffect(() => { endRef.current && endRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' }) }, [messages, phase, interim])

  const say = (text, l = lang) => {
    if (!voiceSupport.tts) return
    if (!hasVoiceFor(l)) setNotice(`No ${l.toUpperCase()} voice is installed on this device, so the answer is shown as text only. You can install a voice in your system language settings.`)
    else setNotice('')
    speak(text, l, { onStart: () => setPhase('speaking'), onEnd: () => setPhase((p) => (p === 'speaking' ? 'idle' : p)) })
  }

  const push = (m) => setMessages((x) => [...x, m])

  const send = async (text, l) => {
    const msg = (text || '').trim()
    if (!msg) return
    const cur = stateRef.current
    const useLang = l || cur.lang
    stopSpeaking()
    setInput(''); setInterim('')
    push({ role: 'user', text: msg })
    setPhase('thinking')
    const history = cur.messages.slice(-8).map((m) => ({ role: m.role, content: m.text }))
    const lastProducts = [...cur.messages].reverse().find((m) => m.role === 'assistant' && m.products && m.products.length)
    try {
      const res = await api('/api/chat', {
        method: 'POST',
        body: { message: msg, language: useLang, history, state: cur.state, context_product_ids: lastProducts ? lastProducts.products.map((p) => p.id) : [], product_id: cur.product ? cur.product.id : null },
      })
      setState(res.state || {})
      push({ role: 'assistant', text: res.reply, products: res.products, suggestions: res.suggestions, compare: res.compare, mode: res.mode })
      if (res.notice) toast(t('ai_unavailable'), 'err')
      setPhase('idle')
      if (cur.ttsOn) say(res.reply, useLang)
    } catch (e) {
      push({ role: 'assistant', text: e.network ? e.message : t('ai_unavailable'), error: true })
      setPhase('idle')
    }
  }

  const explainProduct = async (p) => {
    stopSpeaking()
    setProduct(p)
    push({ role: 'user', text: `${t('explain')}: ${p.name}` })
    setPhase('thinking')
    try {
      const r = await api(`/api/chat/explain/${p.id}`, { method: 'POST', body: { language: stateRef.current.lang } })
      push({ role: 'assistant', text: r.text, products: [p], mode: r.mode })
      if (r.notice) toast(t('ai_unavailable'), 'err')
      setPhase('idle')
      if (stateRef.current.ttsOn) say(r.text)
    } catch (e) { push({ role: 'assistant', text: e.message, error: true }); setPhase('idle') }
  }

  const startListening = (langOverride) => {
    const useLang = langOverride || lang
    if (!langChosen && !langOverride) { setPickLang(true); return }
    if (!voiceSupport.stt) { push({ role: 'assistant', text: t('mic_unsupported'), error: true }); return }
    stopSpeaking()
    if (recRef.current) recRef.current.stop()
    setPhase('listening'); setInterim('')
    recRef.current = listen({
      lang: useLang,
      onInterim: setInterim,
      onFinal: (text) => send(text, useLang),
      onEnd: () => setPhase((p) => (p === 'listening' ? 'idle' : p)),
      onError: (code) => {
        setPhase('idle'); setInterim('')
        const text = ['not-allowed', 'service-not-allowed'].includes(code) ? t('mic_denied')
          : code === 'no-speech' ? t('no_speech')
          : code === 'unsupported' ? t('mic_unsupported')
          : code === 'network' ? 'Speech recognition needs an internet connection. Please check it, or type your question.'
          : code === 'audio-capture' ? 'No microphone was found. Please connect a microphone or type your question.'
          : code === 'aborted' ? '' : 'Could not understand the voice. Please try again or type your question.'
        if (text) push({ role: 'assistant', text, error: true })
      },
    })
  }
  const stopAll = () => { if (recRef.current) recRef.current.stop(); stopSpeaking(); setPhase('idle'); setInterim('') }

  useEffect(() => {
    if (!isOpen || !request) return
    if (stateRef.current.messages.length === 0) push({ role: 'assistant', text: t('welcome_assistant') })
    if (request.product) setProduct(request.product)
    if (request.explain && request.product) explainProduct(request.product)
    else if (request.prompt) send(request.prompt)
    else if (request.listen) setTimeout(() => startListening(), 350)
    // eslint-disable-next-line
  }, [request])

  useEffect(() => { if (!isOpen) stopAll() }, [isOpen]) // eslint-disable-line

  if (!isOpen) return null
  const busy = phase !== 'idle'
  return (
    <section className="assistant" role="dialog" aria-label={t('ask_assistant')}>
      <header className="a-head">
        <div className="a-title">🤖 <span>{t('ask_assistant').replace('🤖 ', '')}</span></div>
        <select aria-label={t('select_language')} value={lang} onChange={(e) => setLang(e.target.value)}>
          {LANGS.map((l) => <option key={l.code} value={l.code}>{l.native}</option>)}
        </select>
        <button className={`icon-btn ${ttsOn ? 'on' : ''}`} onClick={() => { setTtsOn(!ttsOn); if (ttsOn) stopSpeaking() }} aria-pressed={ttsOn} aria-label="Voice answers on/off" title="Voice answers">🔊</button>
        <button className="icon-btn" onClick={close} aria-label="Close assistant">✕</button>
      </header>

      {product && <div className="a-ctx">📌 {product.name} <button className="link" onClick={() => setProduct(null)}>✕</button></div>}

      <div className="a-body" aria-live="polite">
        {pickLang && (
          <div className="lang-pick">
            <h3>{t('voice_lang_title')}</h3><p className="muted">{t('voice_lang_sub')}</p>
            <div className="lang-grid">{LANGS.map((l) => (
              <button key={l.code} className="btn ghost lg" onClick={() => { setLang(l.code); setPickLang(false); setTimeout(() => startListening(l.code), 100) }}>{l.native}</button>
            ))}</div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role} ${m.error ? 'err' : ''}`}>
            <p>{m.text}</p>
            {m.role === 'assistant' && !m.error && voiceSupport.tts && <button className="link" onClick={() => say(m.text)}>{t('replay')}</button>}
            {m.products && m.products.length > 0 && <div className="mini-list">{m.products.map((p) => <MiniProduct key={p.id} p={p} />)}</div>}
            {m.compare && <Link className="btn sm ghost" to={`/compare?ids=${m.products.map((p) => p.id).join(',')}`} onClick={close}>{t('compare')}</Link>}
            {m.suggestions && m.suggestions.length > 0 && i === messages.length - 1 && (
              <div className="chips">{m.suggestions.map((s) => <button key={s.text} className="chip" onClick={() => send(s.text)}>{s.label}</button>)}</div>
            )}
          </div>
        ))}
        {phase === 'thinking' && <div className="bubble assistant"><span className="dots" aria-label={t('thinking')}><i /><i /><i /></span> {t('thinking')}</div>}
        {phase === 'listening' && <div className="bubble user listening"><span className="wave"><i /><i /><i /><i /><i /></span> {interim || t('listening')}</div>}
        {notice && <p className="muted small">{notice}</p>}
        <div ref={endRef} />
      </div>

      <footer className="a-foot">
        <div className="status" aria-live="polite">
          {phase === 'listening' && <span className="pill rec">● {t('listening')}</span>}
          {phase === 'speaking' && <span className="pill">🔊 {t('speaking')}</span>}
          {phase === 'thinking' && <span className="pill">… {t('thinking')}</span>}
          {busy && <button className="btn sm danger" onClick={stopAll}>⏹ {t('stop')}</button>}
        </div>
        <form className="a-input" onSubmit={(e) => { e.preventDefault(); send(input) }}>
          <button type="button" className={`mic ${phase === 'listening' ? 'live' : ''}`} onClick={() => (phase === 'listening' ? stopAll() : startListening())} aria-label={t('tap_speak')} title={t('tap_speak')}>🎤</button>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder={t('type_message')} aria-label={t('type_message')} maxLength={500} />
          <button className="btn" type="submit" disabled={!input.trim()}>{t('send')}</button>
        </form>
      </footer>
    </section>
  )
}
