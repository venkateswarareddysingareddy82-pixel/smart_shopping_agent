import hashlib

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..auth.security import get_optional_user
from ..database import get_db
from ..models import Category, Product, Review, User, ViewHistory
from ..services.products import query_products
from ..services.serializers import product_to_dict

router = APIRouter(tags=["products"])


def category_dict(c: Category, count: int = 0):
    return {"slug": c.slug, "name": c.name, "group": c.group, "emoji": c.emoji, "count": count}


@router.get("/api/products")
def list_products(q: str = "", category: str = "", group: str = "", brand: list[str] = Query(default=[]), min_price: int | None = None,
                  max_price: int | None = None, min_rating: float | None = None, in_stock: bool = False,
                  min_discount: int | None = None, feature: str = "", sort: str = "relevance", page: int = Query(1, ge=1),
                  page_size: int = Query(24, ge=1, le=100), lang: str = "en", db: Session = Depends(get_db),
                  user: User | None = Depends(get_optional_user)):
    res = query_products(db, q=q, category=category, group=group, brands=brand, min_price=min_price, max_price=max_price,
                         min_rating=min_rating, in_stock=in_stock, min_discount=min_discount, feature=feature, sort=sort,
                         page=page, page_size=page_size, lang=lang, user=user)
    parsed = res["parsed"]
    return {"items": [product_to_dict(p) for p in res["items"]], "total": res["total"], "page": res["page"], "page_size": res["page_size"],
            "understood": ({k: parsed.get(k) for k in ("category", "max_price", "min_price", "features", "brands", "source")} if parsed else None)}


@router.get("/api/products/brands")
def brands(category: str = "", db: Session = Depends(get_db)):
    q = db.query(Product.brand).filter(Product.is_active.is_(True))
    if category:
        q = q.filter(Product.category == category)
    return sorted(b for (b,) in q.distinct())


@router.get("/api/products/{pid}")
def product_detail(pid: int, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    p = db.get(Product, pid)
    if not p or not p.is_active:
        raise HTTPException(404, "This product is not available.")
    if user:
        db.add(ViewHistory(user_id=user.id, product_id=pid))
        db.commit()
    similar = db.query(Product).filter(Product.category == p.category, Product.id != pid, Product.is_active.is_(True)).order_by(Product.rating.desc()).limit(4).all()
    return {**product_to_dict(p), "similar": [product_to_dict(s) for s in similar]}


@router.get("/api/categories")
def categories(db: Session = Depends(get_db)):
    counts = dict(db.query(Product.category, func.count(Product.id)).filter(Product.is_active.is_(True)).group_by(Product.category).all())
    return [category_dict(c, counts.get(c.slug, 0)) for c in db.query(Category).order_by(Category.id)]


PALETTES = [("#0E7C66", "#F2A900"), ("#1F3A93", "#7BD3EA"), ("#7A2E65", "#F6C177"), ("#14532D", "#A3E635"), ("#7C2D12", "#FDBA74"), ("#0F4C5C", "#E36414")]


@router.get("/api/images/{pid}/{n}.svg")
def product_image(pid: int, n: int, db: Session = Depends(get_db)):
    """Generated demo product illustration (no external or copyrighted images)."""
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(404, "Image not found.")
    cat = db.query(Category).filter_by(slug=p.category).first()
    emoji = cat.emoji if cat else "🛍️"
    a, b = PALETTES[int(hashlib.md5(p.brand.encode()).hexdigest(), 16) % len(PALETTES)]
    label = ["Front view", "Side view", "In the box"][n % 3]
    name = p.name if len(p.name) <= 30 else p.name[:28] + "…"
    angle = [(0, 0, 1, 1), (1, 0, 0, 1), (0, 1, 1, 0)][n % 3]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="{p.name.replace('"', '')}">
<defs><linearGradient id="g" x1="{angle[0]}" y1="{angle[1]}" x2="{angle[2]}" y2="{angle[3]}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<rect width="400" height="400" fill="url(#g)"/><circle cx="200" cy="170" r="105" fill="#ffffff" fill-opacity=".22"/>
<text x="200" y="205" font-size="110" text-anchor="middle">{emoji}</text>
<text x="200" y="320" font-size="22" font-family="Segoe UI,Arial,sans-serif" font-weight="700" fill="#fff" text-anchor="middle">{name.replace("&", "&amp;")}</text>
<text x="200" y="352" font-size="16" font-family="Segoe UI,Arial,sans-serif" fill="#fff" fill-opacity=".85" text-anchor="middle">{p.brand} · {label} · demo</text></svg>'''
    return Response(svg, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400"})
