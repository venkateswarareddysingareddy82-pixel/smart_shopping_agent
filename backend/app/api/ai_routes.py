from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..ai import llm
from ..ai.assistant import answer_shopping_question, translate_response
from ..ai.language import LANGUAGES, normalize_lang
from ..ai.product_explainer import compare_products, comparison_table, compare_winners, explain_product
from ..ai.recommender import recommend_products, user_signals
from ..auth.security import get_optional_user
from ..config import settings
from ..database import get_db
from ..models import Product, User
from ..schemas import ChatIn, CompareIn, ExplainIn
from ..services.products import query_products
from ..services.serializers import product_to_dict

router = APIRouter(tags=["ai"])


@router.get("/api/ai/status")
def ai_status():
    return {"ai_enabled": llm.available(), "mode": "ai" if llm.available() else "demo", "provider": settings.AI_PROVIDER if llm.available() else None,
            "message": None if llm.available() else "Running in demo mode (no AI key). Search, recommendations and explanations still work using built-in rules."}


@router.get("/api/search")
def search(q: str = Query(min_length=1, max_length=300), lang: str = "en", limit: int = Query(30, ge=1, le=100),
           db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    res = query_products(db, q=q, page_size=limit, lang=normalize_lang(lang), user=user)
    p = res["parsed"] or {}
    return {"items": [product_to_dict(x) for x in res["items"]], "total": res["total"],
            "understood": {k: p.get(k) for k in ("intent", "category", "max_price", "min_price", "features", "brands", "family_size", "source")}}


def _load(db, ids):
    prods = {p.id: p for p in db.query(Product).filter(Product.id.in_(ids), Product.is_active.is_(True))}
    out = [prods[i] for i in ids if i in prods]
    if len(out) < 2:
        raise HTTPException(400, "Please choose at least 2 available products to compare.")
    return out


@router.get("/api/compare")
def compare(ids: str, db: Session = Depends(get_db)):
    try:
        id_list = [int(x) for x in ids.split(",") if x.strip()][:4]
    except ValueError:
        raise HTTPException(400, "Invalid product list.")
    prods = _load(db, id_list)
    return {"products": [product_to_dict(p) for p in prods], "table": comparison_table(prods), "winners": compare_winners(prods)}


@router.post("/api/compare/explain")
def compare_explain(data: CompareIn, db: Session = Depends(get_db)):
    prods = _load(db, data.product_ids)
    return compare_products(prods, data.language, data.priority, data.question)


@router.get("/api/recommendations")
def recommendations(limit: int = Query(8, ge=1, le=24), db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    sig = user_signals(db, user)
    picks, seen = [], set()
    cats = [c for c, _ in sorted(sig["cats"].items(), key=lambda x: -x[1])][:3]
    for c in cats:
        for r in recommend_products(db, {"category": c, "features": ["quality"]}, limit=3, user=user):
            if r["product"].id not in seen:
                seen.add(r["product"].id)
                picks.append(r["product"])
    if len(picks) < limit:  # fill with well-rated, well-priced items from different categories
        by_cat = {}
        for p in db.query(Product).filter(Product.is_active.is_(True), Product.stock > 0, Product.rating >= 4.2).order_by(Product.rating.desc(), Product.review_count.desc()):
            by_cat.setdefault(p.category, p)
        for p in by_cat.values():
            if p.id not in seen and len(picks) < limit:
                seen.add(p.id)
                picks.append(p)
    return {"items": [product_to_dict(p) for p in picks[:limit]], "personalized": bool(cats)}


@router.post("/api/chat")
def chat(data: ChatIn, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    try:
        return answer_shopping_question(db, data.message, normalize_lang(data.language), data.history, data.state,
                                        data.context_product_ids, data.product_id, user)
    except HTTPException:
        raise
    except Exception:  # never crash the UI because of the assistant
        import logging
        logging.getLogger("chat").exception("assistant failure")
        return {"reply": "The AI assistant is temporarily unavailable. You can still search products normally.", "products": [],
                "state": data.state, "suggestions": [], "mode": "demo", "notice": "assistant_error"}


@router.post("/api/chat/explain/{pid}")
def chat_explain(pid: int, data: ExplainIn, db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    if not p or not p.is_active:
        raise HTTPException(404, "This product is not available.")
    alts = db.query(Product).filter(Product.category == p.category, Product.id != pid, Product.is_active.is_(True)).order_by(Product.rating.desc()).limit(2).all()
    return explain_product(p, data.language, data.question, alts)


@router.post("/api/chat/translate")
def chat_translate(payload: dict):
    return {"text": translate_response(str(payload.get("text", ""))[:2000], payload.get("language", "en"))}


@router.get("/api/voice/languages")
def voice_languages():
    return [{"code": c, **v} for c, v in LANGUAGES.items()]


@router.post("/api/voice/query")
def voice_query(data: ChatIn, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    """Voice requests arrive as text (speech-to-text runs in the browser). Returns text ready for text-to-speech."""
    lang = normalize_lang(data.language)
    res = chat(data, db, user)
    res["speech_lang"] = LANGUAGES[lang]["speech"]
    res["speak_text"] = res["reply"]
    return res


@router.post("/api/voice/transcribe")
def voice_transcribe():
    raise HTTPException(501, "Server-side transcription is not configured. The browser's built-in speech recognition is used instead. "
                             "To add a cloud speech API, implement it in backend/app/api/ai_routes.py and frontend/src/services/voice.js.")
