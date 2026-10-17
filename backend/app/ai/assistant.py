"""Conversational shopping assistant: intent -> database retrieval -> localized, fact-only answer."""
import json
import logging

from sqlalchemy.orm import Session

from ..models import Product, SearchHistory
from . import llm
from .facts import category_name, compact_product, feature_params
from .language import LANGUAGES, normalize_lang
from .lexicon import CAT_NAME, FEAT_NAME
from .phrases import msg, reason
from .product_explainer import compare_products, explain_product, compare_winners, _template_compare
from .prompts import ASSISTANT_SYSTEM
from .query_parser import understand_user_query
from .recommender import recommend_products

log = logging.getLogger("assistant")
ASK_CATS = ["smartphones", "laptops", "washing-machines", "refrigerators", "tvs", "shoes"]
PRIORITY_FEATS = {"smartphones": ["camera", "battery", "gaming"], "laptops": ["performance", "battery", "cheap"]}
BUDGET_CHIPS = [10000, 20000, 50000]


def _label(feat, lang):
    return FEAT_NAME[feat].get(lang) or FEAT_NAME[feat]["en"]


def search_products_from_query(db: Session, message: str, lang: str = "en", user=None, limit: int = 5):
    """Spec helper: free-text query -> (parsed intent, recommended products)."""
    brands = [b for (b,) in db.query(Product.brand).distinct()]
    parsed = understand_user_query(message, lang, brands)
    return parsed, recommend_products(db, parsed, limit=limit, user=user)


def translate_response(text: str, target_lang: str) -> str:
    target_lang = normalize_lang(target_lang)
    if target_lang == "en" or not llm.available():
        return text
    try:
        info = LANGUAGES[target_lang]
        return llm.complete(f"Translate the user's text into {info['name']}. Keep numbers, ₹ amounts and product names unchanged. Output only the translation.",
                            [{"role": "user", "content": text}], 600, 0)
    except llm.LLMUnavailable:
        return text


def _clean_history(history):
    msgs = []
    for h in (history or [])[-8:]:
        role = "assistant" if h.get("role") == "assistant" else "user"
        content = str(h.get("content", ""))[:800]
        if not content:
            continue
        if msgs and msgs[-1]["role"] == role:
            msgs[-1]["content"] += "\n" + content
        else:
            msgs.append({"role": role, "content": content})
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    return msgs


def _why(p, reasons, lang):
    return [f"{p.name} {reason(lang, f, **(params or {}))}" for f, params in reasons]


def _pack(recs, lang):
    from ..services.serializers import product_to_dict
    out = []
    for r in recs:
        d = product_to_dict(r["product"])
        d["why"] = _why(r["product"], r["reasons"], lang)
        out.append(d)
    return out


def _chips_category(lang):
    return [{"label": CAT_NAME[c][lang] if lang in CAT_NAME[c] else CAT_NAME[c]["en"], "text": CAT_NAME[c].get(lang, CAT_NAME[c]["en"])} for c in ASK_CATS]


def _chips_budget():
    return [{"label": f"₹{b:,}", "text": str(b)} for b in BUDGET_CHIPS]


def _chips_priority(cat, lang):
    return [{"label": _label(f, lang), "text": _label(f, lang)} for f in PRIORITY_FEATS.get(cat, ["cheap", "quality"])]


def _merge_state(state: dict, parsed: dict) -> dict:
    s = dict(state or {})
    new_cat = parsed.get("category")
    if new_cat and new_cat != s.get("category"):
        s = {"category": new_cat, "max_price": s.get("max_price")}  # new product type: keep budget only
    for k in ("max_price", "min_price", "family_size"):
        if parsed.get(k):
            s[k] = parsed[k]
    if parsed.get("brands"):
        s["brands"] = parsed["brands"]
    feats = list(dict.fromkeys([*(s.get("features") or []), *(parsed.get("features") or [])]))
    if feats:
        s["features"] = feats
    return s


def _best_of(products, feat, lang):
    best, params = None, None
    for p in products:
        pr = feature_params(p, feat) if feat not in ("cheap",) else None
        if feat == "cheap":
            if best is None or p.price < best.price:
                best, params = p, feature_params(p, "cheap")
            continue
        if pr is None:
            continue
        from .facts import metric_for
        _, val = metric_for(p, feat)
        if best is None or (isinstance(val, (int, float)) and val > metric_for(best, feat)[1]):
            best, params = p, pr
    return best, params


def _llm_reply(lang, message, history, intent, crit, products, extra=None):
    info = LANGUAGES[lang]
    system = ASSISTANT_SYSTEM.format(language_name=info["name"], language_native=info["native"], max_words=110)
    data = {"user_message": message, "intent": intent, "user_needs": {k: v for k, v in crit.items() if v},
            "products_shown_to_user": [compact_product(p) for p in products][:5], **(extra or {})}
    task = {"search": "Recommend the products in 2-4 short sentences. Say which one is best for the user's needs and WHY, using only the data.",
            "gift": "Suggest these gift options and explain why they fit the budget and person.",
            "which": "Answer which product is best for the user's question and why, using only the data.",
            "cheaper": "Tell the user about the cheaper alternative and what they give up or keep, using only the data.",
            "info": "Answer the user's question about the product using only the data. If the data does not say, say it is not available."
            }.get(intent, "Answer helpfully using only the data.")
    msgs = _clean_history(history)
    final = f"DATA:\n{json.dumps(data, ensure_ascii=False)}\n\nTask: {task}"
    if msgs and msgs[-1]["role"] == "user":
        msgs[-1]["content"] += "\n\n" + final
    else:
        msgs.append({"role": "user", "content": final})
    return llm.complete(system, msgs, 500)


def answer_shopping_question(db: Session, message: str, lang: str = "en", history=None, state=None,
                             context_ids=None, product_id=None, user=None) -> dict:
    lang = normalize_lang(lang)
    brands = [b for (b,) in db.query(Product.brand).distinct()]
    parsed = understand_user_query(message, lang, brands)
    if parsed.get("maybe_cameras") and not (state or {}).get("category"):
        parsed["category"], parsed["features"] = "cameras", []
    intent = parsed["intent"]
    st = _merge_state(state, parsed)
    ids = [product_id] if product_id else list(context_ids or [])
    ctx = [p for p in (db.get(Product, i) for i in ids) if p and p.is_active]
    res = {"reply": "", "products": [], "state": st, "suggestions": [], "mode": "demo", "intent": intent,
           "parsed": {k: parsed.get(k) for k in ("category", "max_price", "min_price", "features", "brands", "family_size", "source")}}
    if parsed.get("ai_failed"):
        res["notice"] = "ai_unavailable"
    if user and (parsed.get("category") or parsed.get("max_price") or parsed.get("features")):
        db.add(SearchHistory(user_id=user.id, query=message[:300], category=parsed.get("category") or ""))
        db.commit()

    def done(text, products=None, suggestions=None, use_llm=None, recs=None, extra=None, followup=""):
        res["reply"] = text
        shown = recs and [r["product"] for r in recs] or products or []
        if recs:
            res["products"] = _pack(recs, lang)
        elif products:
            from ..services.serializers import product_to_dict
            res["products"] = [product_to_dict(p) for p in products]
        res["suggestions"] = suggestions or []
        if use_llm and llm.available() and not res.get("notice"):
            try:
                res["reply"] = _llm_reply(lang, message, history, use_llm, st, shown, extra)
                if followup:
                    res["reply"] += " " + followup
                res["mode"] = "ai"
            except llm.LLMUnavailable:
                res["notice"] = "ai_unavailable"
        return res

    cat = st.get("category")
    # ---- simple conversational intents -------------------------------------------------
    if intent == "greet":
        return done(msg(lang, "greet"), suggestions=_chips_category(lang))

    if intent == "guide":
        if not cat:
            return done(msg(lang, "ask_category"), suggestions=_chips_category(lang))
        if not st.get("max_price"):
            return done(msg(lang, "ask_budget"), suggestions=_chips_budget())
        if not [f for f in st.get("features", []) if f != "quality"] and not st.get("asked_priority"):
            st["asked_priority"] = True
            opts = ", ".join(_label(f, lang) for f in PRIORITY_FEATS.get(cat, ["cheap", "quality"]))
            return done(msg(lang, "ask_priority", opts=opts), suggestions=_chips_priority(cat, lang))
        intent = "search"

    if intent == "gift":
        if not st.get("max_price") and not cat:
            return done(msg(lang, "gift_ask"), suggestions=_chips_budget())
        recs_all = recommend_products(db, {**st, "features": ["quality"]}, limit=14, user=user)
        seen, recs = set(), []
        for r in recs_all:
            if r["product"].category not in seen:
                seen.add(r["product"].category)
                recs.append(r)
            if len(recs) == 4:
                break
        if not recs:
            return done(msg(lang, "none", budget=msg(lang, "budget_under", max=f"{st['max_price']:,}") if st.get("max_price") else ""))
        names = ", ".join(r["product"].name for r in recs)
        return done(f"{names}", recs=recs, use_llm="gift")

    # ---- context based intents ---------------------------------------------------------
    if intent in ("compare", "explain", "which", "cheaper", "info") and not parsed.get("category"):
        if not ctx:
            return done(msg(lang, "no_context"), suggestions=_chips_category(lang))
        if intent == "compare" or (intent == "which" and len(ctx) >= 2 and not parsed.get("features")):
            if len(ctx) < 2:
                return done(explain_product(ctx[0], lang, message)["text"], products=ctx)
            c = compare_products(ctx[:4], lang, question=message)
            res["compare"] = {"table": c["table"], "winners": c["winners"]}
            res["mode"] = c["mode"]
            return done(c["explanation"], products=ctx[:4])
        if intent in ("explain", "info") or (intent == "which" and len(ctx) == 1):
            if len(ctx) == 1 or intent in ("explain", "info"):
                e = explain_product(ctx[0], lang, message, alternatives=ctx[1:])
                res["mode"] = e["mode"]
                if e.get("notice"):
                    res["notice"] = e["notice"]
                return done(e["text"], products=ctx[:1] if len(ctx) == 1 else ctx[:4])
        if intent == "which":
            feats = [f for f in parsed.get("features", []) if f != "quality"] or ["quality"]
            feat = feats[0]
            if feat == "quality":
                best = max(ctx, key=lambda p: p.rating)
                params = feature_params(best, "quality")
            else:
                best, params = _best_of(ctx, feat, lang)
            if not best:
                return done(msg(lang, "no_data"), products=ctx[:4])
            text = msg(lang, "best_for", feat=_label(feat, lang), name=best.name, v=(params or {}).get("v", ""))
            return done(text, products=[best], use_llm="which", extra={"asked_feature": feat})
        if intent == "cheaper":
            base = ctx[0]
            recs = recommend_products(db, {"category": base.category, "max_price": base.price - 1, "features": ["cheap", "quality"]},
                                      limit=3, user=user, exclude_ids=[p.id for p in ctx])
            if not recs:
                return done(msg(lang, "cheaper_none"), products=[base])
            top = recs[0]["product"]
            return done(msg(lang, "cheaper_found", name=top.name, price=f"{top.price:,}"), recs=recs, use_llm="cheaper")

    # ---- search / recommendation -------------------------------------------------------
    known = cat or st.get("features") or st.get("max_price") or st.get("brands")
    if not known:
        # maybe the words match product names/keywords directly
        from ..services.products import text_search
        hits = text_search(db.query(Product).filter(Product.is_active.is_(True)).all(), message)[:4]
        if hits:
            return done(", ".join(p.name for p in hits), products=hits, use_llm="search")
        return done(msg(lang, "ask_category"), suggestions=_chips_category(lang))

    recs = recommend_products(db, st, limit=4, user=user)
    budget = msg(lang, "budget_under", max=f"{st['max_price']:,}") if st.get("max_price") else ""
    if not recs:
        return done(msg(lang, "none", budget=budget), suggestions=_chips_budget() if st.get("max_price") else _chips_category(lang))
    top = recs[0]
    cat_label = category_name(top["product"].category, lang, top["product"].category.replace("-", " ")) if cat else \
        ", ".join(FEAT_NAME[f].get(lang, f) for f in st.get("features", [])[:2]) or "-"
    whys = _why(top["product"], top["reasons"], lang)
    top_text = whys[0] if whys else top["product"].name
    text = msg(lang, "found", n=len(recs), cat=cat_label, budget=budget, top=top_text.rstrip(".。"))
    if len(whys) > 1:
        text += " " + whys[1] + "."
    suggestions, followup = [], ""
    specific = [f for f in st.get("features", []) if f != "quality"]
    if cat in PRIORITY_FEATS and st.get("max_price") and not specific and not st.get("asked_priority"):
        st["asked_priority"] = True
        opts = ", ".join(_label(f, lang) for f in PRIORITY_FEATS[cat])
        followup = msg(lang, "ask_priority", opts=opts)
        text += " " + followup
        suggestions = _chips_priority(cat, lang)
    elif cat and not st.get("max_price") and not st.get("asked_budget"):
        st["asked_budget"] = True
        followup = msg(lang, "ask_budget")
        text += " " + followup
        suggestions = _chips_budget()
    return done(text, recs=recs, suggestions=suggestions, use_llm="search", followup=followup)
