# Frontend (React + Vite)

```bat
npm install
npm run dev        # http://localhost:5173 (proxies /api to http://127.0.0.1:8000)
npm run build      # production build in dist/
npm run test:ui    # UI tests (backend must be running; set VITE_API_URL=http://127.0.0.1:8000)
```
Production: set `VITE_API_URL` to the deployed backend URL before `npm run build`.

Voice: `src/services/voice.js` (browser Web Speech API; replaceable). Language strings: `src/i18n/index.js`. Assistant UI: `src/components/AssistantPanel.jsx`.
