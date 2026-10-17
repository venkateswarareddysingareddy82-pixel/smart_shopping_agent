from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.security import get_current_user
from ..database import get_db
from ..models import Coupon, Order, OrderItem, User
from ..schemas import CheckoutIn
from ..services.orders import create_order, order_to_dict, set_status

router = APIRouter(tags=["orders"])


def _items(db, o):
    return db.query(OrderItem).filter_by(order_id=o.id).all()


@router.post("/api/orders", status_code=201)
def checkout(data: CheckoutIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Demo checkout: no card numbers are ever collected or stored."""
    order = create_order(db, user, data)
    return order_to_dict(order, _items(db, order))


@router.get("/api/orders")
def my_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [order_to_dict(o, _items(db, o)) for o in db.query(Order).filter_by(user_id=user.id).order_by(Order.id.desc())]


@router.get("/api/orders/{oid}")
def order_detail(oid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(Order, oid)
    if not o or (o.user_id != user.id and not user.is_admin):
        raise HTTPException(404, "Order not found.")
    return order_to_dict(o, _items(db, o))


@router.post("/api/orders/{oid}/cancel")
def cancel_order(oid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(Order, oid)
    if not o or o.user_id != user.id:
        raise HTTPException(404, "Order not found.")
    if o.status not in ("placed", "confirmed"):
        raise HTTPException(400, "This order has already been packed or shipped and can no longer be cancelled.")
    set_status(db, o, "cancelled")
    return order_to_dict(o, _items(db, o))


@router.get("/api/coupons")
def coupons(db: Session = Depends(get_db)):
    return [{"code": c.code, "description": c.description, "percent": c.percent, "min_order": c.min_order}
            for c in db.query(Coupon).filter(Coupon.active.is_(True))]
