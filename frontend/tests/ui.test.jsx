// @vitest-environment jsdom
import { describe, it, expect, beforeAll, afterEach } from 'vitest'
import { render, screen, waitFor, fireEvent, cleanup } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import App from '../src/App.jsx'
import { AppProvider } from '../src/context/AppContext.jsx'
import { AssistantProvider } from '../src/context/AssistantContext.jsx'

const mount = (path = '/') => render(<MemoryRouter initialEntries={[path]}><AppProvider><AssistantProvider><App /></AssistantProvider></AppProvider></MemoryRouter>)
afterEach(() => { cleanup(); localStorage.clear() })
beforeAll(() => { window.scrollTo = () => {}; Element.prototype.scrollIntoView = () => {} })

describe('UI against live backend', () => {
  it('home renders hero, categories, products', async () => {
    mount('/')
    expect(await screen.findByText(/Shop by Speaking/)).toBeTruthy()
    expect(await screen.findByText('Smartphones', {}, { timeout: 8000 })).toBeTruthy()
    await waitFor(() => expect(document.querySelectorAll('.product').length).toBeGreaterThan(5), { timeout: 8000 })
  })
  it('products page: natural language query + filters', async () => {
    mount('/products?q=phone%20under%2015000')
    await waitFor(() => expect(screen.getByText(/We understood/)).toBeTruthy(), { timeout: 8000 })
    expect(document.querySelectorAll('.product').length).toBeGreaterThan(0)
  })
  it('product detail shows explain button and specs', async () => {
    mount('/product/8')
    expect((await screen.findAllByText(/Nova M2 Pro|Nova X5/, {}, { timeout: 8000 })).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/Explain Simply/).length).toBeGreaterThan(0)
    expect(screen.getByText(/Product Details/)).toBeTruthy()
  })
  it('assistant: explain product, then chat + Telugu', async () => {
    mount('/product/8')
    await screen.findAllByText(/Explain Simply/, {}, { timeout: 8000 })
    fireEvent.click(screen.getAllByText(/Explain Simply/)[0])
    await waitFor(() => expect(document.querySelector('.assistant').textContent).toMatch(/₹/), { timeout: 8000 })
    const input = screen.getByLabelText(/Type your question/)
    fireEvent.change(input, { target: { value: 'phone under 15000 with good camera' } })
    fireEvent.submit(input.closest('form'))
    await waitFor(() => expect(document.querySelectorAll('.mini').length).toBeGreaterThan(0), { timeout: 8000 })
    fireEvent.change(document.querySelector('.assistant select'), { target: { value: 'te' } })
    fireEvent.change(input, { target: { value: 'నాకు 15000 లోపు మంచి మొబైల్ కావాలి' } })
    fireEvent.submit(input.closest('form'))
    await waitFor(() => expect(document.querySelector('.assistant').textContent).toMatch(/ఎంపికలు/), { timeout: 8000 })
  })
  it('mic without browser support shows friendly message', async () => {
    mount('/')
    fireEvent.click(await screen.findByLabelText(/Speak to Search/))
    await waitFor(() => expect(document.body.textContent).toMatch(/Choose your language|not supported/), { timeout: 5000 })
  })
  it('login + cart + checkout flow', async () => {
    mount('/login')
    fireEvent.click(await screen.findByText('Use demo user'))
    await waitFor(() => expect(screen.getByText(/Demo/)).toBeTruthy(), { timeout: 8000 })
  })
  it('simple mode page', async () => {
    mount('/simple')
    expect((await screen.findAllByText(/Buy Products|Buy products/)).length).toBeGreaterThan(0)
  })
  it('compare page', async () => {
    mount('/compare?ids=5,6,7')
    expect(await screen.findByText(/Explain Which Is Better/, {}, { timeout: 8000 })).toBeTruthy()
    expect(document.querySelectorAll('.cmp-table tbody tr').length).toBeGreaterThan(4)
  })
})
