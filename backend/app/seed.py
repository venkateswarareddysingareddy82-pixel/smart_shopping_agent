"""Create tables and load DEMO data.   python -m app.seed [--reset] [--export]"""
import json
import sys
from datetime import datetime, timedelta

from .ai.lexicon import CAT_KW
from .auth.security import hash_password
from .config import BACKEND_DIR, PROJECT_DIR, settings
from .database import Base, SessionLocal, engine
from .models import Address, Category, Coupon, Notification, Order, OrderItem, Product, Review, User
from .seed_data import CATEGORIES, COUPONS, G, LAPTOPS, PHONES, SELLERS


def _delivery(price: int) -> str:
    return "Free delivery in 3-5 days" if price >= 499 else "Delivery charge ₹40, arrives in 3-5 days"


def _adv_dis(price, rating, stock, metrics, discount):
    adv, dis = [], []
    m = metrics
    if m.get("camera_mp", 0) >= 50 and "ram_gb" in m:
        adv.append(f"Sharp {m['camera_mp']} MP main camera")
    if m.get("battery_mah", 0) >= 5500:
        adv.append(f"Large {m['battery_mah']} mAh battery for long use")
    if m.get("refresh_hz", 0) >= 120:
        adv.append(f"Smooth {m['refresh_hz']} Hz screen")
    if m.get("ram_gb", 0) >= 8:
        adv.append(f"{m['ram_gb']} GB RAM for smooth multitasking")
    if m.get("star_rating", 0) >= 4:
        adv.append(f"Saves electricity ({m['star_rating']} star)")
    if m.get("sound_score", 0) >= 8:
        adv.append("Very good sound quality")
    if m.get("battery_hours", 0) >= 20 and "ram_gb" not in m:
        adv.append("Long battery life")
    if discount >= 25:
        adv.append(f"{discount}% discount on the original price")
    if rating >= 4.4:
        adv.append("Highly rated by buyers")
    if price <= 10000 and "ram_gb" in m:
        adv.append("Budget friendly")
    if not adv:
        adv.append("Good value for the price")
    if price >= 30000:
        dis.append("Higher price compared with similar products")
    if stock <= 5:
        dis.append(f"Limited stock ({stock} left)")
    if rating < 4.0:
        dis.append("Average buyer rating")
    if 0 < m.get("battery_mah", 99999) < 4500:
        dis.append("Smaller battery")
    if 0 < m.get("camera_mp", 999) < 20 and "ram_gb" in m:
        dis.append("Basic camera")
    if 0 < m.get("ram_gb", 99) <= 4:
        dis.append("Limited RAM; may slow down with heavy apps")
    if m.get("perf_score", 100) < 35 and "ram_gb" in m:
        dis.append("Not meant for heavy gaming or professional work")
    if not dis:
        dis.append("No major drawbacks in the product data")
    return adv[:5], dis[:4]


def _make(i, cat, sub, name, brand, price, orig, rating, reviews, stock, specs, metrics, tags, features, desc):
    adv, dis = _adv_dis(price, rating, stock, metrics, round((orig - price) * 100 / orig))
    kw = " ".join(CAT_KW.get(cat, []) + [brand, name] + tags)
    return Product(name=name, category=cat, subcategory=sub, brand=brand, description=desc, price=price, original_price=orig,
                   discount=round((orig - price) * 100 / orig), rating=rating, review_count=reviews, stock=stock, images=[],
                   specifications=specs, metrics=metrics, features=features, advantages=adv, disadvantages=dis,
                   delivery_information=_delivery(price), seller=SELLERS[i % len(SELLERS)], tags=tags, search_keywords=kw)


def build_products() -> list[Product]:
    out, i = [], 0
    for (name, brand, price, orig, rating, rv, stock, ram, sto, bat, cam, hz, perf, chg, scr, tags) in PHONES:
        specs = {"RAM": f"{ram} GB", "Storage": f"{sto} GB", "Battery": f"{bat} mAh", "Rear Camera": f"{cam} MP",
                 "Display": f"{scr} inch, {hz} Hz", "Processor": f"Performance score {perf}/100", "Charging": f"{chg}W fast charging", "Warranty": "1 year"}
        feats = [f"{bat} mAh battery", f"{cam} MP camera", f"{hz} Hz display", f"{chg}W charging"]
        m = {"ram_gb": ram, "storage_gb": sto, "battery_mah": bat, "camera_mp": cam, "refresh_hz": hz, "perf_score": perf, "charge_w": chg, "screen_inch": scr}
        out.append(_make(i, "smartphones", "5G Smartphone" if "5G" in name else "Smartphone", name, brand, price, orig, rating, rv, stock, specs, m, tags, feats,
                         f"{name} is a demo smartphone with {ram} GB RAM, {sto} GB storage and a {bat} mAh battery."))
        i += 1
    for (name, brand, price, orig, rating, rv, stock, ram, sto, hrs, perf, scr, tags) in LAPTOPS:
        storage_txt = f"{sto // 1024} TB SSD" if sto >= 1024 else f"{sto} GB SSD"
        specs = {"RAM": f"{ram} GB", "Storage": storage_txt, "Battery life": f"Up to {hrs} hours", "Display": f"{scr} inch", "Processor": f"Performance score {perf}/100", "Warranty": "1 year"}
        m = {"ram_gb": ram, "storage_gb": sto, "battery_hours": hrs, "perf_score": perf, "screen_inch": scr}
        out.append(_make(i, "laptops", "Laptop", name, brand, price, orig, rating, rv, stock, specs, m, tags,
                         [f"{ram} GB RAM", storage_txt, f"{hrs} hours battery"], f"{name} is a demo laptop with {ram} GB RAM and {storage_txt}."))
        i += 1
    for (cat, sub, name, brand, price, orig, rating, rv, stock, specs, metrics, tags) in G:
        feats = [f"{k}: {v}" for k, v in list(specs.items())[:4]]
        out.append(_make(i, cat, sub, name, brand, price, orig, rating, rv, stock, specs, metrics, tags, feats, f"{name} - demo product."))
        i += 1
    return out


def seed(reset: bool = False, force: bool = False):
    if reset:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(Product).count() and not force:
            return False
        for slug, name, group, emoji in CATEGORIES:
            db.add(Category(slug=slug, name=name, group=group, emoji=emoji))
        admin = User(name="Demo Admin", email=settings.SEED_ADMIN_EMAIL, password_hash=hash_password(settings.SEED_ADMIN_PASSWORD), is_admin=True)
        user = User(name="Demo User", email=settings.SEED_USER_EMAIL, password_hash=hash_password(settings.SEED_USER_PASSWORD), phone="9000000000")
        db.add_all([admin, user])
        products = build_products()
        db.add_all(products)
        db.flush()
        for p in products:
            p.images = [f"/api/images/{p.id}/{n}.svg" for n in range(3)]
        for code, desc, pct, cap, mn in COUPONS:
            db.add(Coupon(code=code, description=desc, percent=pct, max_discount=cap, min_order=mn))
        db.add(Address(user_id=user.id, full_name="Demo User", phone="9000000000", line1="12-3 Demo Street", city="Guntur", state="Andhra Pradesh", pincode="522001", is_default=True))
        for pid, rating, text in [(1, 4, "Good phone for elders, simple to use."), (6, 5, "Battery lasts all day. Happy with it."), (8, 4, "Camera is good for the price.")]:
            db.add(Review(product_id=pid, user_id=user.id, rating=rating, comment=text))
        # demo order history
        now = datetime.utcnow()
        for k, (pid, status, days) in enumerate([(30, "delivered", 20), (5, "shipped", 2)]):
            p = db.get(Product, pid)
            hist = [{"status": s, "at": (now - timedelta(days=days - j)).isoformat()} for j, s in enumerate(["placed", "confirmed", "packed", "shipped", "out_for_delivery", "delivered"][: (6 if status == "delivered" else 4)])]
            o = Order(user_id=user.id, status=status, subtotal=p.price, discount=0, delivery_fee=0, total=p.price, payment_method="cod",
                      payment_status="paid" if status == "delivered" else "pending", address={"full_name": "Demo User", "line1": "12-3 Demo Street", "city": "Guntur", "state": "Andhra Pradesh", "pincode": "522001", "phone": "9000000000"},
                      status_history=hist, created_at=now - timedelta(days=days))
            db.add(o)
            db.flush()
            db.add(OrderItem(order_id=o.id, product_id=p.id, name=p.name, price=p.price, quantity=1, image=p.images[0]))
        db.add(Notification(user_id=user.id, title="Welcome to Smart Shopping Platform", message="Tap the microphone and speak in your language to find products."))
        db.commit()
        return True
    finally:
        db.close()


def export_json():
    db = SessionLocal()
    try:
        from .services.serializers import product_to_dict
        data = [product_to_dict(p) for p in db.query(Product).all()]
        out = PROJECT_DIR / "database" / "seed" / "products.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Exported {len(data)} products to {out}")
    finally:
        db.close()


if __name__ == "__main__":
    created = seed(reset="--reset" in sys.argv, force="--force" in sys.argv)
    print("Database seeded with demo data." if created else "Database already has data (use --reset to recreate).")
    if "--export" in sys.argv:
        export_json()
