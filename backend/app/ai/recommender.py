"""recommend_products(): budget/feature aware ranking. Never simply picks the most expensive item."""
from sqlalchemy.orm import Session

from ..models import CartItem, Product, SearchHistory, ViewHistory, WishlistItem
from .facts import PEOPLE_DIVISOR, feature_params, metric_for
from .lexicon import FEAT_METRICS

METRIC_FEATS = list(FEAT_METRICS)


def _norm(values: dict, pid: int):
    if pid not in values:
        return None
    lo, hi = min(values.values()), max(values.values())
    return 0.5 if hi == lo else (values[pid] - lo) / (hi - lo)


def user_signals(db: Session, user) -> dict:
    if not user:
        return {"cats": {}, "brands": set()}
    cats: dict[str, float] = {}
    pids = [v.product_id for v in db.query(ViewHistory).filter_by(user_id=user.id).order_by(ViewHistory.id.desc()).limit(20)]
    pids += [c.product_id for c in db.query(CartItem).filter_by(user_id=user.id)]
    wl = [w.product_id for w in db.query(WishlistItem).filter_by(user_id=user.id)]
    brands = set()
    if pids or wl:
        for p in db.query(Product).filter(Product.id.in_(pids + wl)):
            cats[p.category] = cats.get(p.category, 0) + 1
            if p.id in wl:
                brands.add(p.brand)
    for s in db.query(SearchHistory).filter_by(user_id=user.id).order_by(SearchHistory.id.desc()).limit(10):
        if s.category:
            cats[s.category] = cats.get(s.category, 0) + 1
    return {"cats": cats, "brands": brands}


def recommend_products(db: Session, criteria: dict, limit: int = 4, user=None, exclude_ids=()) -> list[dict]:
    """criteria: category, max_price, min_price, brands, features, family_size.
    Returns [{"product": Product, "score": float, "reasons": [(feature, params)]}]."""
    q = db.query(Product).filter(Product.is_active.is_(True), Product.stock > 0)
    if criteria.get("category"):
        q = q.filter(Product.category == criteria["category"])
    if criteria.get("max_price"):
        q = q.filter(Product.price <= criteria["max_price"])
    if criteria.get("min_price"):
        q = q.filter(Product.price >= criteria["min_price"])
    items = [p for p in q.all() if p.id not in set(exclude_ids)]
    brands = [b.lower() for b in criteria.get("brands") or []]
    if brands:
        branded = [p for p in items if p.brand.lower() in brands]
        items = branded or items
    if not items:
        return []

    feats = [f for f in (criteria.get("features") or []) if f in METRIC_FEATS or f in ("cheap", "quality", "kids", "elderly")]
    if not feats:
        feats = ["quality"]  # "a good X" by default: well-rated, not merely the cheapest
    family = criteria.get("family_size")
    prices = {p.id: p.price for p in items}
    ratings = {p.id: p.rating for p in items}
    metric_vals = {}
    for f in METRIC_FEATS:
        vals = {}
        for p in items:
            _, v = metric_for(p, f)
            if isinstance(v, (int, float)):
                vals[p.id] = v
        if vals:
            metric_vals[f] = vals
    signals = user_signals(db, user)

    scored = []
    for p in items:
        score = 0.30 * (p.rating / 5) + 0.08 * min(p.discount, 50) / 50
        if "cheap" not in feats:
            score -= 0.08 * (_norm(prices, p.id) or 0)  # mild value bias, not "most expensive wins"
        for f in feats:
            if f == "cheap":
                score += 1.0 * (1 - (_norm(prices, p.id) or 0))
            elif f == "quality":
                score += 0.8 * (_norm(ratings, p.id) or 0)
            elif f in ("kids", "elderly"):
                score += 0.6 if f in (p.tags or []) else 0
            elif f == "capacity" and family and p.category in PEOPLE_DIVISOR and "capacity" in p.metrics:
                est = p.metrics["capacity"] / PEOPLE_DIVISOR[p.category]
                score += 1.2 * max(0.0, 1 - abs(est - family) / max(family, 1))
            elif f in metric_vals:
                score += 1.0 * (_norm(metric_vals[f], p.id) or 0)
        if family and p.category in PEOPLE_DIVISOR and "capacity" in p.metrics and "capacity" not in feats:
            est = p.metrics["capacity"] / PEOPLE_DIVISOR[p.category]
            score += 1.0 * max(0.0, 1 - abs(est - family) / max(family, 1))
        score += 0.05 * min(signals["cats"].get(p.category, 0), 3) / 3
        if p.brand in signals["brands"]:
            score += 0.03
        scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], x[1].price))

    out = []
    for score, p in scored[:limit]:
        reasons = []
        wanted = list(feats) + (["capacity"] if family and p.category in PEOPLE_DIVISOR else [])
        for f in wanted:
            if f == "capacity" and family:
                params = feature_params(p, "capacity")
            elif f in metric_vals:
                params = feature_params(p, f) if (_norm(metric_vals[f], p.id) or 0) >= 0.5 else None
            else:
                params = feature_params(p, f)
            if params is not None and f not in [r[0] for r in reasons]:
                reasons.append((f, params))
        for extra in ("quality", "discount"):
            if len(reasons) < 3 and extra not in [r[0] for r in reasons]:
                if (extra == "quality" and p.rating >= 4.2) or (extra == "discount" and p.discount >= 20):
                    reasons.append((extra, feature_params(p, extra)))
        out.append({"product": p, "score": round(score, 3), "reasons": reasons[:3]})
    return out
