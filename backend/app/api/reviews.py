from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.security import get_current_user
from ..database import get_db
from ..models import Product, Review, User
from ..schemas import ReviewIn

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


def review_dict(r: Review, name: str):
    return {"id": r.id, "product_id": r.product_id, "user_name": name, "rating": r.rating, "comment": r.comment, "created_at": r.created_at.isoformat()}


@router.get("/product/{pid}")
def product_reviews(pid: int, db: Session = Depends(get_db)):
    rows = db.query(Review, User.name).join(User, User.id == Review.user_id).filter(Review.product_id == pid).order_by(Review.id.desc()).all()
    return [review_dict(r, n) for r, n in rows]


@router.post("/product/{pid}", status_code=201)
def add_review(pid: int, data: ReviewIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(404, "Product not found.")
    if db.query(Review).filter_by(product_id=pid, user_id=user.id).first():
        raise HTTPException(409, "You have already reviewed this product.")
    r = Review(product_id=pid, user_id=user.id, rating=data.rating, comment=data.comment.strip())
    db.add(r)
    p.rating = round((p.rating * p.review_count + data.rating) / (p.review_count + 1), 1)
    p.review_count += 1
    db.commit()
    return review_dict(r, user.name)
