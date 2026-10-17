from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..auth.security import require_admin
from ..database import get_db
from ..models import CartItem, Category, Coupon, Order, OrderItem, Product, Review, User, WishlistItem
from ..schemas import CategoryIn, CouponIn, OrderStatusIn, ProductIn
from ..services.orders import order_to_dict, set_status
from ..services.products import refresh_group_cache
from ..services.serializers import product_to_dict
from .auth import user_dict

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    valid = Order.status != "cancelled"
    sales = db.query(func.coalesce(func.sum(Order.total), 0)).filter(valid).scalar()
    popular = db.query(OrderItem.product_id, OrderItem.name, func.sum(OrderItem.quantity).label("qty")).group_by(OrderItem.product_id, OrderItem.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    low = db.query(Product).filter(Product.is_active.is_(True), Product.stock <= 10).order_by(Product.stock).limit(10).all()
    recent = db.query(Order).order_by(Order.id.desc()).limit(8).all()
    by_status = dict(db.query(Order.status, func.count(Order.id)).group_by(Order.status).all())
    return {"total_sales": int(sales), "total_orders": db.query(Order).count(), "total_users": db.query(User).count(),
            "total_products": db.query(Product).filter(Product.is_active.is_(True)).count(),
            "low_stock": [{"id": p.id, "name": p.name, "stock": p.stock} for p in low],
            "recent_orders": [{"id": o.id, "status": o.status, "total": o.total, "created_at": o.created_at.isoformat(), "user_id": o.user_id} for o in recent],
            "popular_products": [{"id": pid, "name": n, "quantity": int(q)} for pid, n, q in popular],
            "orders_by_status": by_status}


def _apply(p: Product, d: ProductIn, db: Session):
    if not db.query(Category).filter_by(slug=d.category).first():
        raise HTTPException(400, "Unknown category. Create the category first.")
    data = d.model_dump()
    orig = data.pop("original_price") or d.price
    for k, v in data.items():
        setattr(p, k, v)
    p.original_price = max(orig, d.price)
    p.discount = round((p.original_price - p.price) * 100 / p.original_price)


@router.get("/products")
def admin_products(db: Session = Depends(get_db)):
    return [product_to_dict(p) for p in db.query(Product).order_by(Product.id.desc())]


@router.post("/products", status_code=201)
def add_product(data: ProductIn, db: Session = Depends(get_db)):
    p = Product(images=[])
    _apply(p, data, db)
    db.add(p)
    db.flush()
    p.images = [f"/api/images/{p.id}/{n}.svg" for n in range(3)]
    db.commit()
    return product_to_dict(p)


@router.put("/products/{pid}")
def edit_product(pid: int, data: ProductIn, db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(404, "Product not found.")
    _apply(p, data, db)
    db.commit()
    return product_to_dict(p)


@router.patch("/products/{pid}/stock")
def set_stock(pid: int, payload: dict, db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    try:
        stock = int(payload.get("stock"))
    except (TypeError, ValueError):
        raise HTTPException(400, "Stock must be a number.")
    if not p or stock < 0:
        raise HTTPException(400, "Invalid product or stock value.")
    p.stock = stock
    db.commit()
    return product_to_dict(p)


@router.delete("/products/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(404, "Product not found.")
    p.is_active = False  # soft delete keeps past orders intact
    db.query(CartItem).filter_by(product_id=pid).delete()
    db.query(WishlistItem).filter_by(product_id=pid).delete()
    db.commit()
    return {"ok": True}


@router.get("/categories")
def admin_categories(db: Session = Depends(get_db)):
    return [{"id": c.id, "slug": c.slug, "name": c.name, "group": c.group, "emoji": c.emoji} for c in db.query(Category).order_by(Category.id)]


@router.post("/categories", status_code=201)
def add_category(data: CategoryIn, db: Session = Depends(get_db)):
    if db.query(Category).filter_by(slug=data.slug).first():
        raise HTTPException(409, "A category with this slug already exists.")
    c = Category(**data.model_dump())
    db.add(c)
    db.commit()
    refresh_group_cache(db)
    return {"id": c.id, **data.model_dump()}


@router.put("/categories/{cid}")
def edit_category(cid: int, data: CategoryIn, db: Session = Depends(get_db)):
    c = db.get(Category, cid)
    if not c:
        raise HTTPException(404, "Category not found.")
    for k in ("name", "group", "emoji"):
        setattr(c, k, getattr(data, k))
    db.commit()
    refresh_group_cache(db)
    return {"id": c.id, **data.model_dump()}


@router.delete("/categories/{cid}")
def delete_category(cid: int, db: Session = Depends(get_db)):
    c = db.get(Category, cid)
    if not c:
        raise HTTPException(404, "Category not found.")
    if db.query(Product).filter_by(category=c.slug, is_active=True).count():
        raise HTTPException(400, "This category still has products. Move or delete them first.")
    db.delete(c)
    db.commit()
    return {"ok": True}


@router.get("/users")
def users(db: Session = Depends(get_db)):
    counts = dict(db.query(Order.user_id, func.count(Order.id)).group_by(Order.user_id).all())
    return [{**user_dict(u), "is_active": u.is_active, "orders": counts.get(u.id, 0)} for u in db.query(User).order_by(User.id)]


@router.patch("/users/{uid}/active")
def toggle_user(uid: int, payload: dict, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    u = db.get(User, uid)
    if not u:
        raise HTTPException(404, "User not found.")
    if u.id == admin.id:
        raise HTTPException(400, "You cannot disable your own account.")
    u.is_active = bool(payload.get("is_active"))
    db.commit()
    return {"ok": True, "is_active": u.is_active}


@router.get("/orders")
def all_orders(db: Session = Depends(get_db)):
    users = {u.id: u for u in db.query(User)}
    out = []
    for o in db.query(Order).order_by(Order.id.desc()).limit(200):
        d = order_to_dict(o, db.query(OrderItem).filter_by(order_id=o.id).all())
        d["user_name"] = users[o.user_id].name if o.user_id in users else "?"
        d["user_email"] = users[o.user_id].email if o.user_id in users else ""
        out.append(d)
    return out


@router.patch("/orders/{oid}/status")
def order_status(oid: int, data: OrderStatusIn, db: Session = Depends(get_db)):
    o = db.get(Order, oid)
    if not o:
        raise HTTPException(404, "Order not found.")
    set_status(db, o, data.status)
    return order_to_dict(o, db.query(OrderItem).filter_by(order_id=o.id).all())


@router.get("/reviews")
def all_reviews(db: Session = Depends(get_db)):
    rows = db.query(Review, User.name, Product.name).join(User, User.id == Review.user_id).join(Product, Product.id == Review.product_id).order_by(Review.id.desc()).limit(200).all()
    return [{"id": r.id, "product": pn, "user": un, "rating": r.rating, "comment": r.comment, "created_at": r.created_at.isoformat()} for r, un, pn in rows]


@router.delete("/reviews/{rid}")
def delete_review(rid: int, db: Session = Depends(get_db)):
    r = db.get(Review, rid)
    if not r:
        raise HTTPException(404, "Review not found.")
    db.delete(r)
    db.commit()
    return {"ok": True}


@router.get("/coupons")
def admin_coupons(db: Session = Depends(get_db)):
    return [{"id": c.id, "code": c.code, "description": c.description, "percent": c.percent, "max_discount": c.max_discount, "min_order": c.min_order, "active": c.active} for c in db.query(Coupon)]


@router.post("/coupons", status_code=201)
def add_coupon(data: CouponIn, db: Session = Depends(get_db)):
    code = data.code.strip().upper()
    if db.query(Coupon).filter_by(code=code).first():
        raise HTTPException(409, "This coupon code already exists.")
    c = Coupon(**{**data.model_dump(), "code": code})
    db.add(c)
    db.commit()
    return {"id": c.id, **data.model_dump(), "code": code}


@router.put("/coupons/{cid}")
def edit_coupon(cid: int, data: CouponIn, db: Session = Depends(get_db)):
    c = db.get(Coupon, cid)
    if not c:
        raise HTTPException(404, "Coupon not found.")
    for k, v in data.model_dump().items():
        setattr(c, k, v.strip().upper() if k == "code" else v)
    db.commit()
    return {"ok": True}


@router.delete("/coupons/{cid}")
def delete_coupon(cid: int, db: Session = Depends(get_db)):
    c = db.get(Coupon, cid)
    if c:
        db.delete(c)
        db.commit()
    return {"ok": True}
