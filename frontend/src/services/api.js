const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

export const getToken = () => localStorage.getItem('ssp_token')
export const setToken = (t) => (t ? localStorage.setItem('ssp_token', t) : localStorage.removeItem('ssp_token'))

export async function api(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (auth && token) headers.Authorization = `Bearer ${token}`
  let res
  try {
    res = await fetch(BASE + path, { method, headers, body: body !== undefined ? JSON.stringify(body) : undefined })
  } catch {
    const err = new Error('Cannot reach the server. Please check your internet connection and try again.')
    err.network = true
    throw err
  }
  let data = null
  try { data = await res.json() } catch { /* empty body */ }
  if (!res.ok) {
    const err = new Error((data && data.detail && (typeof data.detail === 'string' ? data.detail : 'Please check the details you entered.')) || 'Something went wrong. Please try again.')
    err.status = res.status
    throw err
  }
  return data
}

export const imgUrl = (u) => (u && u.startsWith('/api') ? BASE + u : u)
export const money = (n) => '₹' + Number(n || 0).toLocaleString('en-IN')
