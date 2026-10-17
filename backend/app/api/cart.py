from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.security import get_current_user
from ..database import get_db
from ..models import CartItem, Product, User, WishlistItem
from ..schemas import CartAddIn, CartUpdateIn
from ..services.orders import totals
from ..services.serializers import product_to_dict

router = APIRouter(tags=["cart"])


def _cart(db, user, coupon=""):
    rows = db.query(CartItem).filter_by(user_id=user.id).order_by(CartItem.id).all()
    lines, items = [], []
    for r in rows:
        p = db.get(Product, r.product_id)
        if p and p.is_active:
            lines.append((p, r.quantity))
            items.append({"id": r.id, "quantity": r.quantity, "product": product_to_dict(p)})
    t = totals(db, lines, coupon) if coupon else totals(db, lines)
    return {"items": items, "count": sum(q for _, q in lines), **t}


@router.get("/api/cart")
def get_cart(coupon: str = "", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _cart(db, user, coupon)


@router.post("/api/cart", status_code=201)
def add_to_cart(data: CartAddIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.get(Product, data.product_id)
    if not p or not p.is_active:
        raise HTTPException(404, "This product is not available.")
    if p.stock <= 0:
        raise HTTPException(400, "Sorry, this product is out of stock.")
    item = db.query(CartItem).filter_by(user_id=user.id, product_id=p.id).first()
    qty = (item.quantity if item else 0) + data.quantity
    if qty > p.stock:
        raise HTTPException(400, f"Only {p.stock} available in stock.")
    if item:
        item.quantity = qty
    else:
        db.add(CartItem(user_id=user.id, product_id=p.id, quantity=qty))
    db.commit()
    return _cart(db, user)


@router.put("/api/cart/{product_id}")
def update_cart(product_id: int, data: CartUpdateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(CartItem).filter_by(user_id=user.id, product_id=product_id).first()
    p = db.get(Product, product_id)
    if not item or not p:
        raise HTTPException(404, "This item is not in your cart.")
    if data.quantity > p.stock:
        raise HTTPException(400, f"Only {p.stock} available in stock.")
    item.quantity = data.quantity
    db.commit()
    return _cart(db, user)


@router.delete("/api/cart/{product_id}")
def remove_from_cart(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(CartItem).filter_by(user_id=user.id, product_id=product_id).delete()
    db.commit()
    return _cart(db, user)


@router.get("/api/wishlist")
def get_wishlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ids = [w.product_id for w in db.query(WishlistItem).filter_by(user_id=user.id).order_by(WishlistItem.id.desc())]
    prods = {p.id: p for p in db.query(Product).filter(Product.id.in_(ids), Product.is_active.is_(True))} if ids else {}
    return [product_to_dict(prods[i]) for i in ids if i in prods]


@router.post("/api/wishlist/{product_id}", status_code=201)
def add_wishlist(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Product, product_id):
        raise HTTPException(404, "This product is not available.")
    if not db.query(WishlistItem).filter_by(user_id=user.id, product_id=product_id).first():
        db.add(WishlistItem(user_id=user.id, product_id=product_id))
        db.commit()
    return {"ok": True}


@router.delete("/api/wishlist/{product_id}")
def remove_wishlist(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(WishlistItem).filter_by(user_id=user.id, product_id=product_id).delete()
    db.commit()
    return {"ok": True}
