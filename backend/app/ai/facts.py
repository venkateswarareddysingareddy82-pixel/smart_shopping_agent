"""Helpers that turn database product rows into plain facts (shared by recommender, explainer, assistant)."""
from .lexicon import CAT_NAME, FEAT_METRICS

PEOPLE_DIVISOR = {"washing-machines": 2.0, "refrigerators": 75.0, "microwave-ovens": 9.0}
UNITS = {"camera_mp": "MP", "battery_mah": "mAh", "battery_hours": "hours", "storage_gb": "GB", "refresh_hz": "Hz",
         "screen_inch": "inch", "sound_score": "/10", "star_rating": "star", "ram_gb": "GB RAM"}


def metric_for(product, feat: str):
    for key in FEAT_METRICS.get(feat, []):
        if key in (product.metrics or {}):
            return key, product.metrics[key]
    return None, None


def people_range(category: str, value: float):
    div = PEOPLE_DIVISOR.get(category)
    if not div:
        return None
    lo = max(1, int(value / div))
    return lo, lo + 1


def feature_params(product, feat: str) -> dict | None:
    """Values used to fill the localized reason templates. None if the product has no data for the feature."""
    if feat == "cheap":
        return {"v": f"{product.price:,}"}
    if feat == "quality":
        return {"v": f"{product.rating:g}"} if product.rating else None
    if feat == "discount":
        return {"v": product.discount} if product.discount else None
    if feat in ("kids", "elderly"):
        return {} if feat in (product.tags or []) else None
    key, val = metric_for(product, feat)
    if key is None:
        return None
    if key == "perf_score":
        text = (product.specifications or {}).get("Processor") or (product.specifications or {}).get("Processor Type")
        return {"v": text or str(val)}
    if key == "capacity":
        unit = (product.metrics or {}).get("capacity_unit", "")
        rng = people_range(product.category, val) or (1, 2)
        return {"v": f"{val:g} {unit}".strip(), "lo": rng[0], "hi": rng[1]}
    unit = UNITS.get(key, "")
    return {"v": (f"{val:g}/10" if unit == "/10" else f"{val:g} {unit}".strip())}


def category_name(slug: str, lang: str, fallback: str = "") -> str:
    names = CAT_NAME.get(slug, {})
    return names.get(lang) or names.get("en") or fallback or slug.replace("-", " ")


def compact_product(p) -> dict:
    """Facts handed to the LLM. Only database values."""
    return {"id": p.id, "name": p.name, "brand": p.brand, "category": p.category, "price_inr": p.price,
            "original_price_inr": p.original_price, "discount_percent": p.discount, "rating": p.rating,
            "review_count": p.review_count, "stock": p.stock, "specifications": p.specifications,
            "features": p.features, "advantages": p.advantages, "disadvantages": p.disadvantages,
            "delivery": p.delivery_information, "seller": p.seller, "tags": p.tags, "description": p.description}
