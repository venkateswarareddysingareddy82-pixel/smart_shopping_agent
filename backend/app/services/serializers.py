from ..models import Product

GROUP_CACHE: dict[str, str] = {}


def product_to_dict(p: Product, group: str | None = None) -> dict:
    return {
        "id": p.id, "name": p.name, "category": p.category, "subcategory": p.subcategory, "group": group or GROUP_CACHE.get(p.category, ""),
        "brand": p.brand, "description": p.description, "price": p.price, "original_price": p.original_price,
        "discount": p.discount, "rating": p.rating, "review_count": p.review_count, "stock": p.stock,
        "in_stock": p.stock > 0, "images": p.images or [], "image": (p.images or [""])[0],
        "specifications": p.specifications or {}, "features": p.features or [], "advantages": p.advantages or [],
        "disadvantages": p.disadvantages or [], "delivery_information": p.delivery_information, "seller": p.seller,
        "tags": p.tags or [], "search_keywords": p.search_keywords,
        "metrics": p.metrics or {}, "is_active": p.is_active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
