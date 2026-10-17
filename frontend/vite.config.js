import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backend = env.BACKEND_URL || 'http://127.0.0.1:8000'
  return {
    plugins: [react()],
    test: { environment: 'jsdom', testTimeout: 20000, include: ['tests/**/*.test.jsx'] },
    server: { port: 5173, proxy: { '/api': { target: backend, changeOrigin: true } } },
  }
})
