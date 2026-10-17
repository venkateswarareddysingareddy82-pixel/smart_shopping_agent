# Backend (FastAPI)

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
pytest -q
```
Reads `.env` from `backend/` or the project root. See the main README for variables. Interactive docs: http://localhost:8000/docs

AI logic lives in `app/ai/` (kept in small modules): `query_parser` (understand), `recommender`, `product_explainer`, `assistant` (chat orchestration), `llm` (optional LLM client), `lexicon`/`phrases`/`language` (multilingual data).
