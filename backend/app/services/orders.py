from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Address, CartItem, Coupon, Notification, Order, OrderItem, Product

STATUS_FLOW = ["placed", "confirmed", "packed", "shipped", "out_for_delivery", "delivered"]
ALL_STATUSES = STATUS_FLOW + ["cancelled"]
FREE_DELIVERY_ABOVE = 499
DELIVERY_FEE = 40


def notify(db: Session, user_id: int, title: str, message: str = ""):
    db.add(Notification(user_id=user_id, title=title, message=message))


def calc_coupon(db: Session, code: str, subtotal: int) -> tuple[int, Coupon | None]:
    code = (code or "").strip().upper()
    if not code:
        return 0, None
    c = db.query(Coupon).filter(Coupon.code == code, Coupon.active.is_(True)).first()
    if not c:
        raise HTTPException(400, "This coupon code is not valid.")
    if subtotal < c.min_order:
        raise HTTPException(400, f"This coupon works on orders above ₹{c.min_order:,}.")
    return min(subtotal * c.percent // 100, c.max_discount), c


def totals(db: Session, lines: list[tuple[Product, int]], coupon_code: str = "") -> dict:
    subtotal = sum(p.price * q for p, q in lines)
    discount, coupon = calc_coupon(db, coupon_code, subtotal)
    fee = 0 if subtotal - discount >= FREE_DELIVERY_ABOVE or subtotal == 0 else DELIVERY_FEE
    return {"subtotal": subtotal, "discount": discount, "delivery_fee": fee, "total": subtotal - discount + fee,
            "coupon_code": coupon.code if coupon else ""}


def order_to_dict(o: Order, items: list[OrderItem]) -> dict:
    return {"id": o.id, "status": o.status, "subtotal": o.subtotal, "discount": o.discount, "delivery_fee": o.delivery_fee,
            "total": o.total, "coupon_code": o.coupon_code, "payment_method": o.payment_method, "payment_status": o.payment_status,
            "address": o.address, "status_history": o.status_history, "created_at": o.created_at.isoformat(), "user_id": o.user_id,
            "items": [{"product_id": i.product_id, "name": i.name, "price": i.price, "quantity": i.quantity, "image": i.image} for i in items]}


def create_order(db: Session, user, payload) -> Order:
    if payload.buy_now_product_id:
        p = db.get(Product, payload.buy_now_product_id)
        if not p or not p.is_active:
            raise HTTPException(404, "This product is no longer available.")
        lines = [(p, payload.buy_now_quantity)]
    else:
        items = db.query(CartItem).filter_by(user_id=user.id).all()
        lines = []
        for ci in items:
            p = db.get(Product, ci.product_id)
            if p and p.is_active:
                lines.append((p, ci.quantity))
        if not lines:
            raise HTTPException(400, "Your cart is empty. Please add a product first.")
    for p, q in lines:
        if p.stock < q:
            raise HTTPException(400, f"Sorry, only {p.stock} of '{p.name}' left in stock." if p.stock else f"Sorry, '{p.name}' is out of stock.")
    if payload.address_id:
        a = db.get(Address, payload.address_id)
        if not a or a.user_id != user.id:
            raise HTTPException(404, "Address not found.")
        addr = {c: getattr(a, c) for c in ("full_name", "phone", "line1", "line2", "city", "state", "pincode")}
    elif payload.address:
        addr = payload.address.model_dump(exclude={"is_default"})
    else:
        raise HTTPException(400, "Please choose or add a delivery address.")
    t = totals(db, lines, payload.coupon_code)
    now = datetime.utcnow()
    order = Order(user_id=user.id, status="placed", subtotal=t["subtotal"], discount=t["discount"], delivery_fee=t["delivery_fee"],
                  total=t["total"], coupon_code=t["coupon_code"], payment_method=payload.payment_method,
                  payment_status="paid" if payload.payment_method == "demo_online" else "pending", address=addr,
                  status_history=[{"status": "placed", "at": now.isoformat()}])
    db.add(order)
    db.flush()
    for p, q in lines:
        p.stock -= q
        db.add(OrderItem(order_id=order.id, product_id=p.id, name=p.name, price=p.price, quantity=q, image=(p.images or [""])[0]))
    if not payload.buy_now_product_id:
        db.query(CartItem).filter_by(user_id=user.id).delete()
    notify(db, user.id, f"Order #{order.id} placed", f"Total ₹{order.total:,}. We will keep you updated.")
    db.commit()
    return order


def set_status(db: Session, order: Order, status: str):
    if status not in ALL_STATUSES:
        raise HTTPException(400, "Unknown order status.")
    if order.status in ("delivered", "cancelled") and status != order.status:
        raise HTTPException(400, f"This order is already {order.status}.")
    if status == "cancelled":
        for it in db.query(OrderItem).filter_by(order_id=order.id):
            p = db.get(Product, it.product_id)
            if p:
                p.stock += it.quantity
    order.status = status
    order.status_history = [*order.status_history, {"status": status, "at": datetime.utcnow().isoformat()}]
    if status == "delivered" and order.payment_method == "cod":
        order.payment_status = "paid"
    notify(db, order.user_id, f"Order #{order.id} is {status.replace('_', ' ')}", "")
    db.commit()
