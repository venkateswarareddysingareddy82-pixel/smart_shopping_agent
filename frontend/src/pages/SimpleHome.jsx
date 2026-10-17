import { useNavigate } from 'react-router-dom'
import { LANGS } from '../i18n'
import { useApp } from '../context/AppContext'
import { useAssistant } from '../context/AssistantContext'
import { useState } from 'react'

export default function SimpleHome() {
  const { t, lang, setLang, setSimple } = useApp()
  const { open } = useAssistant()
  const nav = useNavigate()
  const [pick, setPick] = useState(false)
  const tiles = [
    { icon: '🛒', label: t('buy_products'), go: () => nav('/products') },
    { icon: '🎤', label: t('speak_search'), go: () => open({ listen: true }), accent: true },
    { icon: '📦', label: t('my_orders'), go: () => nav('/orders') },
    { icon: '❤️', label: t('my_wishlist'), go: () => nav('/wishlist') },
    { icon: '🤖', label: t('ask_assistant'), go: () => open({}) },
    { icon: '🌐', label: t('select_language'), go: () => setPick(!pick) },
  ]
  return (
    <div className="page">
      <h1 className="simple-title">{t('simple_mode')}</h1>
      <div className="tiles">{tiles.map((x, i) => (
        <button key={i} className={`tile ${x.accent ? 'accent' : ''}`} onClick={x.go}><span className="ti">{x.icon}</span><span>{x.label.replace(/^\S+\s/, '')}</span></button>
      ))}</div>
      {pick && <div className="lang-grid big">{LANGS.map((l) => <button key={l.code} className={`btn lg ${l.code === lang ? '' : 'ghost'}`} onClick={() => { setLang(l.code); setPick(false) }}>{l.native}</button>)}</div>}
      <p className="center"><button className="link" onClick={() => { setSimple(false); nav('/') }}>Switch to normal mode</button></p>
    </div>
  )
}
