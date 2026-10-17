"""explain_product() and compare_products(): simple-language explanations built ONLY from database facts."""
import json

from . import llm
from .facts import category_name, compact_product, feature_params, metric_for
from .language import LANGUAGES, normalize_lang, normalize_text
from .lexicon import FEAT_NAME, INTENT_KW
from .phrases import msg, reason
from .prompts import ASSISTANT_SYSTEM, EXPLAIN_TASK

POINT_ORDER = ["camera", "battery", "gaming", "storage", "display", "sound", "energy", "capacity", "kids", "elderly"]


def _system(lang: str, max_words: int = 140) -> str:
    info = LANGUAGES[lang]
    return ASSISTANT_SYSTEM.format(language_name=info["name"], language_native=info["native"], max_words=max_words)


def product_points(product, lang: str, limit: int = 3) -> list[str]:
    out = []
    for feat in POINT_ORDER:
        params = feature_params(product, feat)
        if params is not None:
            out.append(f"{product.name} {reason(lang, feat, **params)}")
        if len(out) >= limit:
            break
    return out


def _template_explain(product, lang: str, question: str, category_label: str) -> str:
    parts = [msg(lang, "i_intro", name=product.name, brand=product.brand, cat=category_label)]
    if product.discount:
        parts.append(msg(lang, "i_price_disc", price=f"{product.price:,}", d=product.discount, orig=f"{product.original_price:,}"))
    else:
        parts.append(msg(lang, "i_price", price=f"{product.price:,}"))
    points = product_points(product, lang)
    parts.extend(f"{x}." if lang not in ("hi", "bn") else f"{x}।" for x in points) if points else parts.append(msg(lang, "i_noinfo"))
    if question and any(normalize_text(w) in normalize_text(question) for w in INTENT_KW["elder"]):
        parts.append(msg(lang, "elder_yes" if "elderly" in (product.tags or []) else "elder_unknown"))
    if product.stock <= 0:
        parts.append(msg(lang, "i_stock_out"))
    elif product.stock <= 5:
        parts.append(msg(lang, "i_stock_low", n=product.stock))
    r = f"{product.rating:g}"
    if product.rating >= 4.2:
        parts.append(msg(lang, "i_good", r=r))
    elif product.rating >= 3.7:
        parts.append(msg(lang, "i_ok", r=r))
    elif product.rating > 0:
        parts.append(msg(lang, "i_low", r=r))
    return " ".join(parts)


def explain_product(product, lang: str = "en", question: str = "", alternatives=None) -> dict:
    lang = normalize_lang(lang)
    label = category_name(product.category, lang, product.category.replace("-", " "))
    if llm.available():
        try:
            data = {"product": compact_product(product),
                    "alternatives": [compact_product(a) for a in (alternatives or [])[:2]]}
            task = EXPLAIN_TASK.format(question=f'The user also asked: "{question}"' if question else "")
            text = llm.complete(_system(lang, 170), [{"role": "user", "content": f"DATA:\n{json.dumps(data, ensure_ascii=False)}\n\n{task}"}], 600)
            return {"text": text, "mode": "ai"}
        except llm.LLMUnavailable:
            return {"text": _template_explain(product, lang, question, label), "mode": "demo", "notice": "ai_unavailable"}
    return {"text": _template_explain(product, lang, question, label), "mode": "demo"}


COMPARE_FEATS = ["camera", "battery", "gaming", "storage", "display", "sound", "energy", "capacity"]


def comparison_table(products) -> list[dict]:
    rows = [
        {"feature": "Price", "values": [f"₹{p.price:,}" for p in products]},
        {"feature": "Discount", "values": [f"{p.discount}%" if p.discount else "-" for p in products]},
        {"feature": "Rating", "values": [f"{p.rating:g}/5 ({p.review_count})" for p in products]},
        {"feature": "Brand", "values": [p.brand for p in products]},
    ]
    keys = []
    for p in products:
        for k in (p.specifications or {}):
            if k not in keys:
                keys.append(k)
    for k in keys[:12]:
        rows.append({"feature": k, "values": [str((p.specifications or {}).get(k, "-")) for p in products]})
    rows.append({"feature": "Stock", "values": [("In stock" if p.stock > 0 else "Out of stock") for p in products]})
    return rows


def compare_winners(products) -> dict:
    winners = {}
    if len(products) < 2:
        return winners
    for feat in COMPARE_FEATS:
        vals = []
        for p in products:
            key, v = metric_for(p, feat)
            if isinstance(v, (int, float)):
                vals.append((v, p))
        if len(vals) >= 2 and len({v for v, _ in vals}) > 1:
            best = max(vals, key=lambda x: x[0])[1]
            winners[feat] = {"product_id": best.id, "name": best.name, "params": feature_params(best, feat)}
    return winners


def _template_compare(products, winners, lang: str, priority: str | None) -> str:
    parts = [msg(lang, "compare_head")]
    cheapest = min(products, key=lambda p: p.price)
    best_rated = max(products, key=lambda p: p.rating)
    parts.append(msg(lang, "compare_price", name=cheapest.name, price=f"{cheapest.price:,}"))
    parts.append(msg(lang, "compare_rating", name=best_rated.name, r=f"{best_rated.rating:g}"))
    order = ([priority] if priority in winners else []) + [f for f in COMPARE_FEATS if f in winners and f != priority]
    for feat in order[:4]:
        w = winners[feat]
        v = (w["params"] or {}).get("v", "")
        parts.append(msg(lang, "best_for", feat=FEAT_NAME.get(feat, {}).get(lang) or FEAT_NAME[feat]["en"], name=w["name"], v=v))
    if len(parts) == 3 and not winners:
        parts.append(msg(lang, "no_data"))
    return " ".join(parts)


def compare_products(products, lang: str = "en", priority: str | None = None, question: str = "") -> dict:
    lang = normalize_lang(lang)
    table = comparison_table(products)
    winners = compare_winners(products)
    result = {"table": table, "winners": winners, "products": [p.id for p in products]}
    if llm.available():
        try:
            data = {"products": [compact_product(p) for p in products], "priority": priority}
            task = ("Compare these products for the user in simple language. Say which is better for which need "
                    "(price, camera, battery, performance, family size, etc.) using only the data. " +
                    (f'The user asked: "{question}"' if question else ""))
            result["explanation"] = llm.complete(_system(lang, 180), [{"role": "user", "content": f"DATA:\n{json.dumps(data, ensure_ascii=False)}\n\n{task}"}], 700)
            result["mode"] = "ai"
            return result
        except llm.LLMUnavailable:
            result["notice"] = "ai_unavailable"
    result["explanation"] = _template_compare(products, winners, lang, priority)
    result["mode"] = "demo"
    return result
