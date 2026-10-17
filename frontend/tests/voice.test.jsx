// @vitest-environment jsdom
import { it, expect } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import React from 'react'

const spoken = []
let usedLang = null
window.scrollTo = () => {}; Element.prototype.scrollIntoView = () => {}
class FakeSR {
  start() { usedLang = this.lang; setTimeout(() => { this.onresult({ resultIndex: 0, results: [Object.assign([{ transcript: 'నాకు 20 వేల లోపు మంచి ఫోన్ కావాలి' }], { isFinal: true })] }); this.onend() }, 50) }
  stop() {}
}
window.SpeechRecognition = FakeSR
window.SpeechSynthesisUtterance = class { constructor(t) { this.text = t } }
window.speechSynthesis = { cancel() {}, getVoices: () => [{ lang: 'te-IN', name: 'Fake Telugu' }], speak(u) { spoken.push(u); setTimeout(() => { u.onstart && u.onstart(); u.onend && u.onend() }, 10) } }

it('mic -> language pick -> Telugu STT -> chat -> Telugu TTS', async () => {
  const { default: App } = await import('../src/App.jsx')
  const { AppProvider } = await import('../src/context/AppContext.jsx')
  const { AssistantProvider } = await import('../src/context/AssistantContext.jsx')
  render(<MemoryRouter><AppProvider><AssistantProvider><App /></AssistantProvider></AppProvider></MemoryRouter>)
  fireEvent.click(await screen.findByLabelText(/Speak to Search/))
  fireEvent.click(await screen.findByText('తెలుగు', { selector: '.lang-grid button' }))
  await waitFor(() => expect(usedLang).toBe('te-IN'), { timeout: 3000 })
  await waitFor(() => expect(document.querySelectorAll('.mini').length).toBeGreaterThan(0), { timeout: 8000 })
  const text = document.querySelector('.assistant').textContent
  expect(text).toMatch(/నాకు 20 వేల/)       // transcript shown
  expect(text).toMatch(/20,000 లోపు/)        // budget understood, Telugu answer
  await waitFor(() => expect(spoken.length).toBeGreaterThan(0))
  expect(spoken[0].lang).toBe('te-IN')
  expect(spoken[0].voice.name).toBe('Fake Telugu')
})
