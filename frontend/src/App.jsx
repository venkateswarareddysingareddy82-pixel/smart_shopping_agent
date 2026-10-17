import { Route, Routes, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import Header from './components/Header'
import AssistantPanel from './components/AssistantPanel'
import { Fab, Footer, Protected, Toasts } from './components/Misc'
import { useApp } from './context/AppContext'
import Home from './pages/Home'
import SimpleHome from './pages/SimpleHome'
import Products from './pages/Products'
import ProductDetail from './pages/ProductDetail'
import { Cart, Checkout } from './pages/Cart'
import { Orders, OrderDetail } from './pages/Orders'
import Wishlist from './pages/Wishlist'
import Compare from './pages/Compare'
import { Login, Register } from './pages/Auth'
import Profile from './pages/Profile'
import Admin from './pages/Admin'

export default function App() {
  const { simple } = useApp()
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return (
    <div className={simple ? 'simple' : ''}>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/simple" element={<SimpleHome />} />
          <Route path="/products" element={<Products />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Protected><Cart /></Protected>} />
          <Route path="/checkout" element={<Protected><Checkout /></Protected>} />
          <Route path="/orders" element={<Protected><Orders /></Protected>} />
          <Route path="/orders/:id" element={<Protected><OrderDetail /></Protected>} />
          <Route path="/wishlist" element={<Protected><Wishlist /></Protected>} />
          <Route path="/profile" element={<Protected><Profile /></Protected>} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<Protected admin><Admin /></Protected>} />
          <Route path="*" element={<div className="page"><h1>Page not found</h1></div>} />
        </Routes>
      </main>
      <Footer />
      <AssistantPanel />
      <Fab />
      <Toasts />
    </div>
  )
}
