from .conftest import login


def test_health(client):
    r = client.get("/api/health").json()
    assert r["status"] == "ok" and r["ai_enabled"] is False


def test_auth_flow(client):
    r = client.post("/api/auth/register", json={"name": "Test Person", "email": "t1@example.com", "password": "Passw0rd!x"})
    assert r.status_code == 201
    assert client.post("/api/auth/register", json={"name": "Test Person", "email": "t1@example.com", "password": "Passw0rd!x"}).status_code == 409
    assert client.post("/api/auth/login", json={"email": "t1@example.com", "password": "wrong"}).status_code == 401
    h = login(client, "t1@example.com", "Passw0rd!x")
    assert client.get("/api/auth/me", headers=h).json()["email"] == "t1@example.com"
    assert client.post("/api/auth/logout", headers=h).status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_products_filters_sort(client):
    r = client.get("/api/products?category=smartphones&sort=price_asc").json()
    prices = [p["price"] for p in r["items"]]
    assert prices == sorted(prices) and r["total"] >= 8
    assert all(p["price"] <= 15000 for p in client.get("/api/products?category=smartphones&max_price=15000").json()["items"])
    assert client.get("/api/products?brand=Nova&category=smartphones").json()["total"] >= 2
    assert client.get("/api/products/1").json()["id"] == 1
    assert client.get("/api/products/99999").status_code == 404
    assert len(client.get("/api/categories").json()) >= 30
    assert client.get("/api/images/1/0.svg").headers["content-type"].startswith("image/svg")


def test_natural_language_search(client):
    r = client.get("/api/search", params={"q": "I need a phone under 15000 with a good camera"}).json()
    assert r["understood"]["category"] == "smartphones" and r["understood"]["max_price"] == 15000
    assert r["items"] and all(p["price"] <= 15000 for p in r["items"])
    r = client.get("/api/search", params={"q": "నాకు 20 వేల లోపు మంచి ఫోన్ కావాలి", "lang": "te"}).json()
    assert r["understood"]["category"] == "smartphones" and r["understood"]["max_price"] == 20000
    r = client.get("/api/search", params={"q": "Show me a laptop for coding under 50000"}).json()
    assert r["understood"]["category"] == "laptops" and r["items"][0]["price"] <= 50000
    r = client.get("/api/search", params={"q": "नमस्ते मुझे 25 हज़ार तक का वॉशिंग मशीन चाहिए"}).json()
    assert r["understood"]["category"] == "washing-machines" and r["understood"]["max_price"] == 25000
    assert client.get("/api/search", params={"q": "zzzzqqq"}).status_code == 200


def test_cart_wishlist_checkout_orders(client, user_h):
    assert client.get("/api/cart").status_code == 401
    r = client.post("/api/cart", json={"product_id": 5, "quantity": 2}, headers=user_h).json()
    assert r["count"] == 2
    r = client.put("/api/cart/5", json={"quantity": 1}, headers=user_h).json()
    assert r["count"] == 1
    assert client.post("/api/cart", json={"product_id": 6, "quantity": 1}, headers=user_h).json()["count"] == 2
    assert client.delete("/api/cart/6", headers=user_h).json()["count"] == 1
    assert client.post("/api/wishlist/8", headers=user_h).status_code == 201
    assert any(p["id"] == 8 for p in client.get("/api/wishlist", headers=user_h).json())
    client.delete("/api/wishlist/8", headers=user_h)
    assert client.get("/api/wishlist", headers=user_h).json() == []
    before = client.get("/api/products/5").json()["stock"]
    addr = client.get("/api/users/me/addresses", headers=user_h).json()[0]["id"]
    assert client.post("/api/orders", json={"address_id": addr, "coupon_code": "NOPE"}, headers=user_h).status_code == 400
    o = client.post("/api/orders", json={"address_id": addr, "payment_method": "demo_online", "coupon_code": "WELCOME10"}, headers=user_h)
    assert o.status_code == 201, o.text
    o = o.json()
    assert o["discount"] > 0 and o["status"] == "placed"
    assert client.get("/api/products/5").json()["stock"] == before - 1
    assert client.get("/api/cart", headers=user_h).json()["count"] == 0
    assert client.get("/api/orders", headers=user_h).json()[0]["id"] == o["id"]
    assert client.post("/api/orders", json={"address_id": addr}, headers=user_h).status_code == 400  # empty cart
    c = client.post(f"/api/orders/{o['id']}/cancel", headers=user_h).json()
    assert c["status"] == "cancelled" and client.get("/api/products/5").json()["stock"] == before
    r = client.post("/api/orders", json={"address_id": addr, "buy_now_product_id": 2, "buy_now_quantity": 1}, headers=user_h)
    assert r.status_code == 201


def test_reviews(client, user_h):
    r = client.post("/api/reviews/product/10", json={"rating": 5, "comment": "Great"}, headers=user_h)
    assert r.status_code == 201
    assert client.post("/api/reviews/product/10", json={"rating": 5}, headers=user_h).status_code == 409
    assert client.get("/api/reviews/product/10").json()[0]["rating"] == 5


def test_authorization(client, user_h, admin_h):
    assert client.get("/api/admin/dashboard", headers=user_h).status_code == 403
    assert client.get("/api/admin/dashboard").status_code == 401
    d = client.get("/api/admin/dashboard", headers=admin_h).json()
    assert d["total_products"] >= 85 and d["total_users"] >= 2
    admin_order = client.post("/api/auth/register", json={"name": "Other User", "email": "o@example.com", "password": "Passw0rd!x"}).json()["token"]
    first = client.get("/api/orders", headers=user_h).json()[0]["id"]
    assert client.get(f"/api/orders/{first}", headers={"Authorization": f"Bearer {admin_order}"}).status_code == 404


def test_admin_crud(client, admin_h):
    body = {"name": "Test Product X", "category": "smartphones", "brand": "Nova", "price": 9000, "original_price": 10000, "stock": 3}
    p = client.post("/api/admin/products", json=body, headers=admin_h)
    assert p.status_code == 201 and p.json()["discount"] == 10
    pid = p.json()["id"]
    assert client.put(f"/api/admin/products/{pid}", json={**body, "price": 8000}, headers=admin_h).json()["price"] == 8000
    assert client.patch(f"/api/admin/products/{pid}/stock", json={"stock": 50}, headers=admin_h).json()["stock"] == 50
    assert client.delete(f"/api/admin/products/{pid}", headers=admin_h).status_code == 200
    assert client.get(f"/api/products/{pid}").status_code == 404
    assert client.post("/api/admin/products", json={**body, "category": "nope"}, headers=admin_h).status_code == 400
    assert client.post("/api/admin/coupons", json={"code": "tst20", "percent": 20}, headers=admin_h).status_code == 201
    assert client.post("/api/admin/categories", json={"slug": "test-cat", "name": "Test Cat", "group": "Electronics"}, headers=admin_h).status_code == 201
    assert len(client.get("/api/admin/users", headers=admin_h).json()) >= 3
    oid = client.get("/api/admin/orders", headers=admin_h).json()[0]["id"]
    st = client.patch(f"/api/admin/orders/{oid}/status", json={"status": "shipped"}, headers=admin_h)
    assert st.status_code in (200, 400)
    assert len(client.get("/api/admin/reviews", headers=admin_h).json()) >= 1


def test_compare(client):
    r = client.get("/api/compare?ids=5,6,7").json()
    assert len(r["products"]) == 3 and r["table"]
    e = client.post("/api/compare/explain", json={"product_ids": [5, 6, 7], "language": "te"}).json()
    assert e["explanation"] and e["mode"] == "demo"
    assert client.get("/api/compare?ids=5").status_code == 400


def test_chat_languages_and_context(client):
    r = client.post("/api/chat", json={"message": "Show me phones under 20000", "language": "en"}).json()
    assert r["products"] and r["mode"] == "demo"
    ids = [p["id"] for p in r["products"]]
    r2 = client.post("/api/chat", json={"message": "Which one has the best camera?", "language": "en", "context_product_ids": ids, "state": r["state"]}).json()
    assert "camera" in r2["reply"].lower() and r2["products"]
    r3 = client.post("/api/chat", json={"message": "What is the difference between these?", "language": "en", "context_product_ids": ids[:2]}).json()
    assert r3.get("compare")
    te = client.post("/api/chat", json={"message": "నాకు 15000 లోపు మంచి మొబైల్ కావాలి.", "language": "te"}).json()
    assert te["products"] and any("\u0c00" <= ch <= "\u0c7f" for ch in te["reply"])
    follow = client.post("/api/chat", json={"message": "బ్యాటరీ మరియు కెమెరా.", "language": "te", "state": te["state"]}).json()
    assert follow["products"] and follow["state"]["category"] == "smartphones"
    for lang in ("hi", "ta", "kn", "ml", "bn", "mr"):
        x = client.post("/api/chat", json={"message": "hello", "language": lang}).json()
        assert x["reply"] and x["reply"] != client.post("/api/chat", json={"message": "hello", "language": "en"}).json()["reply"]
    wm = client.post("/api/chat", json={"message": "నా అమ్మ కోసం తక్కువ ధరలో మంచి వాషింగ్ మెషీన్ కావాలి", "language": "te"}).json()
    assert wm["state"]["category"] == "washing-machines" and wm["products"]
    fam = client.post("/api/chat", json={"message": "I don't know which refrigerator is good. Suggest one for a family of four.", "language": "en"}).json()
    assert fam["products"] and fam["state"].get("family_size") == 4
    guide = client.post("/api/chat", json={"message": "I don't know what to buy. Ask me questions.", "language": "en"}).json()
    assert not guide["products"] and guide["suggestions"]
    gift = client.post("/api/chat", json={"message": "I need a gift for my father under 5000", "language": "en"}).json()
    assert gift["products"]
    cheaper = client.post("/api/chat", json={"message": "Find a cheaper alternative", "language": "en", "context_product_ids": [8]}).json()
    assert cheaper["products"] and cheaper["products"][0]["price"] < 19999
    voice = client.post("/api/voice/query", json={"message": "phone under 10000", "language": "hi"}).json()
    assert voice["speech_lang"] == "hi-IN" and voice["speak_text"]


def test_explain_product_all_languages(client):
    for lang in ("en", "te", "hi", "ta", "kn", "ml", "bn", "mr"):
        r = client.post("/api/chat/explain/37", json={"language": lang, "question": "Is this good for my mother?"}).json()
        assert len(r["text"]) > 40
    te = client.post("/api/chat/explain/37", json={"language": "te"}).json()["text"]
    assert "7" in te and "₹" in te


def test_recommendations(client, user_h):
    assert client.get("/api/recommendations").json()["items"]
    client.get("/api/products/20", headers=user_h)
    assert client.get("/api/recommendations", headers=user_h).json()["personalized"] is True


def test_no_invented_facts(client):
    r = client.post("/api/chat", json={"message": "Show me phones under 12000", "language": "en"}).json()
    for p in r["products"]:
        assert p["price"] <= 12000
