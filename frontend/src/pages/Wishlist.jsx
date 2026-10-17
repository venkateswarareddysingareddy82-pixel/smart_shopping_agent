import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { useApp } from '../context/AppContext'
import { ProductGrid } from '../components/ProductCard'

export default function Wishlist() {
  const { t, wishIds } = useApp()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  useEffect(() => { api('/api/wishlist').then(setItems).catch((e) => setError(e.message)).finally(() => setLoading(false)) }, [wishIds.length])
  return <div className="page"><h1>{t('my_wishlist')}</h1><ProductGrid items={items} loading={loading} error={error} /></div>
}
