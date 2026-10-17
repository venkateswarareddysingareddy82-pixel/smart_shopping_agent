"""Product listing/search service (filters, sorting, natural-language search)."""
import re

from sqlalchemy.orm import Session

from ..ai.language import normalize_text
from ..ai.query_parser import understand_user_query
from ..ai.recommender import recommend_products
from ..models import Category, Product
from .serializers import GROUP_CACHE

STOP = {"for", "under", "with", "the", "and", "from", "show", "need", "want", "get", "buy", "good", "best", "please", "find",
        "suggest", "something", "below", "within", "around", "about", "that", "have", "has"}


def refresh_group_cache(db: Session):
    GROUP_CACHE.clear()
    for c in db.query(Category).all():
        GROUP_CACHE[c.slug] = c.group


def tokens_of(text: str) -> list[str]:
    return [t for t in re.findall(r"\w+", normalize_text(text), flags=re.UNICODE) if len(t) >= 2 and t not in STOP and not t.isdigit()]


def text_search(products: list[Product], q: str) -> list[Product]:
    toks = tokens_of(q)
    if not toks:
        return products
    scored = []
    for p in products:
        name, brand = normalize_text(p.name), normalize_text(p.brand)
        cat = normalize_text(p.category.replace("-", " "))
        tags = normalize_text(" ".join(p.tags or []))
        kw = normalize_text(p.search_keywords or "")
        desc = normalize_text(p.description or "")
        s = 0.0
        for t in toks:
            s += (3 if t in name else 0) + (3 if t in brand else 0) + (2 if t in cat else 0) + (2 if t in tags else 0) \
                 + (1 if t in kw else 0) + (0.5 if t in desc else 0)
        if s > 0:
            scored.append((s + p.rating / 10, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored]


def smart_search(db: Session, q: str, lang: str = "en", user=None, limit: int = 60) -> tuple[list[Product], dict]:
    """Natural-language search: structured (category/budget/features) if understood, else keyword."""
    brands = [b for (b,) in db.query(Product.brand).distinct()]
    parsed = understand_user_query(q, lang, brands)
    if parsed.get("maybe_cameras"):
        parsed["category"], parsed["features"] = "cameras", []
    structured = parsed.get("category") or parsed.get("max_price") or parsed.get("min_price") or parsed.get("brands") \
        or [f for f in parsed.get("features", []) if f not in ("quality",)]
    if structured and parsed["intent"] in ("search", "which", "cheaper", "gift"):
        recs = recommend_products(db, parsed, limit=limit, user=user)
        if recs:
            return [r["product"] for r in recs], parsed
    active = db.query(Product).filter(Product.is_active.is_(True)).all()
    return text_search(active, q), parsed


SORTS = {
    "price_asc": lambda p: p.price, "price_desc": lambda p: -p.price, "rating": lambda p: -p.rating,
    "discount": lambda p: -p.discount, "newest": lambda p: -(p.created_at.timestamp() if p.created_at else 0),
    "popular": lambda p: -p.review_count,
}


def query_products(db: Session, *, q="", category="", group="", brands=None, min_price=None, max_price=None, min_rating=None,
                   in_stock=False, min_discount=None, feature="", sort="relevance", page=1, page_size=24, lang="en", user=None) -> dict:
    parsed = None
    if q.strip():
        items, parsed = smart_search(db, q, lang, user)
    else:
        items = db.query(Product).filter(Product.is_active.is_(True)).order_by(Product.id).all()
    out = []
    brand_set = {b.lower() for b in (brands or [])}
    for p in items:
        if category and p.category != category:
            continue
        if group and GROUP_CACHE.get(p.category) != group:
            continue
        if brand_set and p.brand.lower() not in brand_set:
            continue
        if min_price is not None and p.price < min_price:
            continue
        if max_price is not None and p.price > max_price:
            continue
        if min_rating is not None and p.rating < min_rating:
            continue
        if in_stock and p.stock <= 0:
            continue
        if min_discount is not None and p.discount < min_discount:
            continue
        if feature and feature.lower() not in " ".join([*(p.features or []), *(p.tags or [])]).lower():
            continue
        out.append(p)
    if sort in SORTS:
        out.sort(key=SORTS[sort])
    total = len(out)
    start = (page - 1) * page_size
    return {"items": out[start:start + page_size], "total": total, "page": page, "page_size": page_size, "parsed": parsed}
