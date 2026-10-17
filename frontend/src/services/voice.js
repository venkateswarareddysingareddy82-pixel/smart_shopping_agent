// Replaceable voice layer. To use a cloud speech API (Google/Azure/Whisper...) keep the same
// interface: listen({lang, onInterim, onFinal, onError, onEnd}) -> {stop} and speak(text, lang, cbs).
const SR = typeof window !== 'undefined' ? window.SpeechRecognition || window.webkitSpeechRecognition : null

export const speechLang = { en: 'en-IN', te: 'te-IN', hi: 'hi-IN', ta: 'ta-IN', kn: 'kn-IN', ml: 'ml-IN', bn: 'bn-IN', mr: 'mr-IN' }

export const voiceSupport = {
  stt: !!SR,
  tts: typeof window !== 'undefined' && 'speechSynthesis' in window,
}

export function listen({ lang, onInterim, onFinal, onError, onEnd }) {
  if (!SR) { onError && onError('unsupported'); onEnd && onEnd(); return { stop() {} } }
  const rec = new SR()
  rec.lang = speechLang[lang] || 'en-IN'
  rec.interimResults = true
  rec.continuous = false
  rec.maxAlternatives = 1
  let finalText = ''
  let failed = false
  rec.onresult = (e) => {
    let interim = ''
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const r = e.results[i]
      if (r.isFinal) finalText += r[0].transcript
      else interim += r[0].transcript
    }
    onInterim && onInterim(finalText + interim)
  }
  rec.onerror = (e) => { failed = true; onError && onError(e.error) }
  rec.onend = () => {
    onEnd && onEnd()
    if (!failed && finalText.trim()) onFinal && onFinal(finalText.trim())
    else if (!failed) onError && onError('no-speech')
  }
  try { rec.start() } catch { onError && onError('start-failed') }
  return { stop: () => { try { rec.stop() } catch { /* ignore */ } } }
}

function pickVoice(lang) {
  const code = speechLang[lang] || 'en-IN'
  const voices = window.speechSynthesis.getVoices()
  return voices.find((v) => v.lang.replace('_', '-').toLowerCase() === code.toLowerCase())
    || voices.find((v) => v.lang.toLowerCase().startsWith(lang))
}

export function speak(text, lang, { onStart, onEnd, onError } = {}) {
  if (!voiceSupport.tts || !text) { onEnd && onEnd(); return }
  const synth = window.speechSynthesis
  synth.cancel()
  // Chrome stops long utterances: speak sentence by sentence.
  const parts = text.replace(/\s+/g, ' ').match(/[^.!?।]+[.!?।]?/g) || [text]
  let i = 0
  const next = () => {
    if (i >= parts.length) { onEnd && onEnd(); return }
    const u = new SpeechSynthesisUtterance(parts[i++].trim())
    u.lang = speechLang[lang] || 'en-IN'
    const v = pickVoice(lang)
    if (v) u.voice = v
    u.rate = 0.95
    u.onstart = () => { if (i === 1) onStart && onStart() }
    u.onend = next
    u.onerror = (e) => { if (e.error !== 'interrupted' && e.error !== 'canceled') onError && onError(e.error); onEnd && onEnd() }
    synth.speak(u)
  }
  next()
}

export function stopSpeaking() { if (voiceSupport.tts) window.speechSynthesis.cancel() }
export function hasVoiceFor(lang) {
  if (!voiceSupport.tts) return false
  return !!pickVoice(lang)
}
