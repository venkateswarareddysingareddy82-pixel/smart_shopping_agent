# 🎤 Smart Shopping Platform

**An AI-powered, multilingual e-commerce platform where anyone can shop simply by speaking in their own language** — even if they don't know product names, technical specifications, or how a normal shopping website works.

> All brands, products, prices and ratings are **fictional demo data**. No real payments are processed.

---

## 1. Problem statement
Online shopping assumes you can read English, type product names, and understand specs like "5000 mAh, 33W fast charging" or "1200 RPM". Elderly users, first-time online shoppers and people more comfortable in Telugu, Hindi, Tamil, etc. are left behind.

## 2. Solution
Tap the 🎤 microphone, say what you need in your language — *"నాకు 15000 లోపు మంచి మొబైల్ కావాలి"* — and the assistant understands budget, category and needs, searches the product database, explains **why** each product fits **in your language**, and can read the answer aloud. A big-button **Simple Mode** removes complexity.

## 3. Main features
Browse · natural-language search · filters & sorting · product details & gallery · comparison · cart · wishlist · checkout (demo payment) · address book · order history & tracking timeline · reviews/ratings · coupons · notifications · JWT login · full **admin panel** (products, stock, categories, users, orders, reviews, coupons, sales dashboard) · responsive & accessible UI.

## 4. AI features
| Feature | What it does |
|---|---|
| `understand_user_query()` | Turns free text in any supported language into category, budget, brand, needs, family size, intent |
| `recommend_products()` | Scores products by budget, needs (camera/battery/gaming/…), rating, discount, family-size fit, and the user's history/wishlist/cart. **Never just "most expensive"** and always explains why |
| `explain_product()` | "🧠 Explain Simply": what it is, who it suits, features, pros/cons, value — in the selected language |
| `compare_products()` | Table + "Explain which is better" |
| `answer_shopping_question()` | Context-aware chat ("which one has the best camera?" refers to the products just shown), guided "ask me questions" flow, gift help, cheaper alternatives |
| `translate_response()` | Optional LLM translation helper |

**Honesty rule:** the assistant only uses facts stored in the database (price, specs, stock, rating, warranty, delivery…). Missing data → *"This information is not available."* The LLM prompt enforces this, and demo mode builds sentences purely from database fields.

### Two modes (the app never crashes without AI)
* **Demo mode (default, no key needed):** built-in rule engine understands queries in all 8 languages (budget words like `వేల`, `हज़ार`, `lakh`, categories, features) and produces localized answers from templates + database facts.
* **AI mode:** set `AI_API_KEY` → an LLM does deeper understanding and writes more natural answers (still grounded in database data). If the API fails, the app silently falls back to demo mode and shows *"The AI assistant is temporarily unavailable. You can still search products normally."*

## 5. Voice features
* 🎤 microphone on the header, hero, product pages and inside the chat; language picker appears on first use
* Browser **Speech Recognition** (speech → text) with live transcript, listening indicator, stop button
* Browser **Speech Synthesis** (text → speech) in the selected language, speaking indicator, 🔊 replay per answer, voice on/off
* Friendly handling of: mic permission denied, no microphone, no speech heard, unsupported browser, offline, no installed voice for a language
* Replaceable voice layer: `frontend/src/services/voice.js` (swap in Google/Azure/Whisper later; `/api/voice/transcribe` is a documented stub)

> ✅ Use **Google Chrome or Microsoft Edge** for voice. Firefox has no speech recognition. Speech recognition needs internet (the browser sends audio to its speech service). Indian-language *voice output* needs a voice installed in your OS (Windows: Settings → Time & language → Speech → Add voices).

## 6. Supported languages
English, Telugu (తెలుగు), Hindi (हिन्दी), Tamil (தமிழ்), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Bengali (বাংলা), Marathi (मराठी).
Language affects: voice recognition, AI replies, product explanations, recommendations, chatbot, instructions, error messages and key UI labels.
**Add a language:** add words to `backend/app/ai/lexicon.py`, sentences to `backend/app/ai/phrases.py`, `LANGUAGES` in `backend/app/ai/language.py`, and UI strings in `frontend/src/i18n/index.js`.

## 7. Tech stack
React 18 + Vite · React Router · plain CSS · Python **FastAPI** · SQLAlchemy 2 · **PostgreSQL** (SQLite fallback for easy local use) · PyJWT + PBKDF2 password hashing · httpx (LLM client) · pytest + Vitest.

## 8. Architecture
```
Browser (React)                       FastAPI backend                        Data
┌───────────────┐  speech→text   ┌──────────────────────────┐
│ Mic / Chat UI │ ─────────────▶ │ /api/chat  /api/voice    │   ┌──────────────┐
│ (Web Speech)  │                │  ai/assistant.py         │──▶│ PostgreSQL / │
│ product pages │ ◀───────────── │  ai/query_parser.py      │   │ SQLite       │
│ cart, admin   │  text + cards  │  ai/recommender.py       │   └──────────────┘
└──────┬────────┘                │  ai/product_explainer.py │
       │ text→speech             │  ai/llm.py ──▶ (optional LLM API)
       ▼                         │  api/* REST, auth, admin │
  speechSynthesis                └──────────────────────────┘
```

## 9. Folder structure
```
smart-shopping-platform/
├── frontend/            React + Vite app (components, pages, context, services, i18n, tests)
├── backend/
│   ├── app/
│   │   ├── api/         routes: auth, users, products, cart(+wishlist), orders, reviews, ai_routes, admin
│   │   ├── ai/          assistant, query_parser, recommender, product_explainer, language, lexicon, phrases, prompts, llm
│   │   ├── auth/        password hashing, JWT, admin guard
│   │   ├── models/      SQLAlchemy models
│   │   ├── schemas/     Pydantic request models
│   │   ├── services/    product search/listing, orders/totals, serializers
│   │   ├── seed_data.py / seed.py   demo catalogue + seeding
│   │   └── main.py
│   ├── tests/           pytest API tests
│   └── requirements.txt
├── database/seed/       products.json (export of the demo catalogue)
├── docker-compose.yml   PostgreSQL + backend + frontend
├── start.bat / start.sh one-click start
├── .env.example  .gitignore  README.md
```

## 10. Installation (Windows) — the easy way
**Required software**
* Python **3.10 – 3.12** (https://www.python.org — tick *Add Python to PATH*)
* Node.js **18 or newer** (https://nodejs.org)
* Google Chrome / Edge

**Steps**
1. Extract the ZIP.
2. Double-click **`start.bat`**.

It creates `.env`, a Python virtual environment, installs everything, creates and seeds the database, starts both servers and opens the browser.

## 11. Manual installation
### Backend
```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
(macOS/Linux: `source venv/bin/activate`)

### Frontend
```bat
cd frontend
npm install
npm run dev
```

## 12. Environment setup
Copy `.env.example` → `.env` (project root or `backend/`). All variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | empty = SQLite file; or `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT signing key — **set a long random value** before deploying |
| `FRONTEND_URL`, `BACKEND_URL`, `CORS_ORIGINS` | URLs / allowed origins |
| `AI_API_KEY` | **optional** LLM key (never exposed to the browser) |
| `AI_PROVIDER` / `AI_MODEL` / `AI_BASE_URL` | `anthropic` (default) or `openai`-compatible |
| `VITE_API_URL` | backend URL for production frontend builds (empty in dev) |
| `AUTO_SEED`, `SEED_*` | demo data and dev-only demo credentials |

> 🔑 **To enable the AI mode you must add your own `AI_API_KEY` to `.env` manually.** Without it everything still works in demo mode.

## 13. Database setup
* **Default:** SQLite — nothing to install. File `backend/smart_shopping.db` is created on first start.
* **PostgreSQL:** create a database, set `DATABASE_URL=postgresql://user:password@localhost:5432/smart_shopping`.
* **Seeding:** automatic on first start (`AUTO_SEED=true`). Manually: `cd backend && python -m app.seed` (`--reset` wipes and recreates, `--export` writes `database/seed/products.json`).
* The demo catalogue has **105 products in 31 categories** across Electronics, Home Appliances, Fashion, Grocery, Beauty and Agriculture. Add more in the Admin panel or in `backend/app/seed_data.py`.

## 14. Running locally
| What | URL |
|---|---|
| Website | http://localhost:5173 |
| API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/health |

**Docker alternative:** `docker compose up --build` → website at http://localhost:8080 (PostgreSQL included).

## 15. Demo credentials (development only)
| Role | Email | Password |
|---|---|---|
| User | `user@example.com` | `User@12345` |
| Admin | `admin@example.com` | `Admin@12345` |

These exist only for local demos. Change them via `SEED_*` variables **before first run**, or change the passwords/delete the accounts in any real deployment. The login page also has one-click demo buttons.

## 16. How to try it (demo script)
1. Open the site, click the big 🎤, choose **తెలుగు**, allow the microphone.
2. Say: *"నాకు 20 వేల లోపు మంచి ఫోన్ కావాలి"* → results appear and the answer is spoken in Telugu.
3. Say *"బ్యాటరీ మరియు కెమెరా"* → refined recommendations (conversation context is kept).
4. Open a product → **🧠 Explain Simply** / **🎤 Ask About This Product** ("Is this good for my mother?").
5. Tick ⚖️ on 2–3 phones → Compare → **Explain Which Is Better**.
6. Switch to **Simple Mode** (header) for the big-button interface.
7. Log in as the admin → manage products, stock, orders, coupons.
Other examples: *"I don't know which refrigerator is good. Suggest one for a family of four."* · *"Show me a laptop for coding under 50000."* · *"I don't know what to buy. Ask me questions."* · *"I need a gift for my father under 5000."*

Coupons: `WELCOME10` (orders ≥ ₹999), `SMART5`, `FESTIVE15` (orders ≥ ₹5000).

## 17. API documentation
Interactive docs: `/docs`. Main routes:
```
POST /api/auth/register | /login | /logout        GET /api/auth/me
GET/PUT /api/users/me   /me/addresses   /me/notifications
GET  /api/products (q, category, brand, min_price, max_price, min_rating, in_stock, min_discount, feature, sort, page)
GET  /api/products/{id}    /api/products/brands    /api/categories    /api/images/{id}/{n}.svg
GET  /api/search?q=...&lang=te                      natural-language search
GET/POST/PUT/DELETE /api/cart      /api/wishlist
POST /api/orders   GET /api/orders   GET /api/orders/{id}   POST /api/orders/{id}/cancel   GET /api/coupons
GET/POST /api/reviews/product/{id}
GET  /api/compare?ids=1,2,3        POST /api/compare/explain
GET  /api/recommendations
POST /api/chat                      conversational assistant
POST /api/chat/explain/{product_id} "Explain simply"
POST /api/voice/query               voice request (text in, speak_text + speech_lang out)
GET  /api/voice/languages           GET /api/ai/status
/api/admin/*   dashboard, products, categories, users, orders, reviews, coupons (admin only)
```

## 18. Testing
```bash
cd backend  && pytest -q          # 13 API tests: auth, products, filters, NL search (en/te/hi), cart, wishlist,
                                  # checkout, orders, reviews, authorization, admin CRUD, compare, chat in 8 languages
cd frontend && npm run test:ui    # 9 UI tests (needs the backend running on :8000 and VITE_API_URL=http://127.0.0.1:8000):
                                  # home, search, product page, assistant, simulated microphone→Telugu→TTS, login, simple mode, compare
```
**Test status when this ZIP was built:** all 13 backend tests and 9 UI tests passed; the production build succeeded. The microphone/speech tests use a **mocked** browser speech API (a headless test machine has no real microphone) — please do one real voice test in Chrome/Edge on your laptop.

## 19. Security notes
Passwords hashed with PBKDF2-SHA256 (200k iterations, per-user salt) · JWT auth · admin-only routes enforced server-side · users can only see/modify their own cart, orders and addresses · Pydantic validation on every request · CORS allow-list · API keys only on the server · **no card numbers or payment credentials are collected or stored** (demo checkout only) · `.env` is git-ignored.

## 20. Screenshots
_Add your screenshots here:_ `docs/home.png`, `docs/voice.png`, `docs/product.png`, `docs/admin.png`

## 21. Future improvements
Server-side speech (Whisper/Google/Azure) for better Indian-language accuracy · image-based product search · more languages (Odia, Gujarati, Punjabi…) · real payment gateway (sandbox) · seller accounts · push/WhatsApp notifications · embeddings-based semantic search · offline/PWA mode.

## 22. Deployment
* **Frontend → Vercel/Netlify:** root = `frontend`, build `npm run build`, output `dist`, env `VITE_API_URL=https://your-backend-url`. (`vercel.json` handles SPA routing.)
* **Backend → Render / Railway / Cloud Run:** root = `backend`, build `pip install -r requirements.txt`, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (a `Procfile` and `Dockerfile` are included). Set `DATABASE_URL` (PostgreSQL), `SECRET_KEY`, `FRONTEND_URL` (your Vercel URL), optional `AI_API_KEY`, and strong `SEED_*` passwords (or `AUTO_SEED=false` and create your own admin).
* **Database:** any managed PostgreSQL (Neon, Supabase, Render, Railway). Tables are created automatically on start.
* No localhost URLs are hard-coded; everything uses environment variables.

## 23. GitHub instructions
```bash
cd smart-shopping-platform
git init
git add .
git status            # make sure .env, node_modules, venv and *.db are NOT listed
git commit -m "Smart Shopping Platform - initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/smart-shopping-platform.git
git push -u origin main
```

## Troubleshooting
* **Mic does nothing / "not supported"** → use Chrome or Edge, open via `http://localhost` (not a file), allow the microphone in the address-bar lock icon.
* **No spoken answer in Telugu etc.** → install that language's voice in Windows speech settings; the answer is still shown as text.
* **Port already in use** → close old terminals, or change ports (`--port 8001` and `BACKEND_URL` in `.env`).
* **`pip install` fails for psycopg2** → use Python 3.10–3.12, or remove that line from `requirements.txt` if you only use SQLite.
* **Reset all data** → stop servers, delete `backend/smart_shopping.db`, start again.
