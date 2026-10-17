from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..ai.language import normalize_lang
from ..auth.security import get_current_user
from ..database import get_db
from ..models import Address, Notification, User
from ..schemas import AddressIn, ProfileIn
from .auth import user_dict

router = APIRouter(prefix="/api/users", tags=["users"])


def addr_dict(a: Address):
    return {c: getattr(a, c) for c in ("id", "full_name", "phone", "line1", "line2", "city", "state", "pincode", "is_default")}


@router.put("/me")
def update_profile(data: ProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.name is not None:
        user.name = data.name.strip()
    if data.phone is not None:
        user.phone = data.phone
    if data.preferred_language:
        user.preferred_language = normalize_lang(data.preferred_language)
    db.commit()
    return user_dict(user)


@router.get("/me/addresses")
def list_addresses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [addr_dict(a) for a in db.query(Address).filter_by(user_id=user.id).order_by(Address.is_default.desc(), Address.id)]


@router.post("/me/addresses", status_code=201)
def add_address(data: AddressIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    first = db.query(Address).filter_by(user_id=user.id).count() == 0
    if data.is_default or first:
        db.query(Address).filter_by(user_id=user.id).update({"is_default": False})
    a = Address(user_id=user.id, **{**data.model_dump(), "is_default": data.is_default or first})
    db.add(a)
    db.commit()
    return addr_dict(a)


@router.put("/me/addresses/{aid}")
def edit_address(aid: int, data: AddressIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.get(Address, aid)
    if not a or a.user_id != user.id:
        raise HTTPException(404, "Address not found.")
    if data.is_default:
        db.query(Address).filter_by(user_id=user.id).update({"is_default": False})
    for k, v in data.model_dump().items():
        setattr(a, k, v)
    db.commit()
    return addr_dict(a)


@router.delete("/me/addresses/{aid}")
def delete_address(aid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.get(Address, aid)
    if not a or a.user_id != user.id:
        raise HTTPException(404, "Address not found.")
    db.delete(a)
    db.commit()
    return {"ok": True}


@router.get("/me/notifications")
def notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Notification).filter_by(user_id=user.id).order_by(Notification.id.desc()).limit(50).all()
    return [{"id": n.id, "title": n.title, "message": n.message, "is_read": n.is_read, "created_at": n.created_at.isoformat()} for n in rows]


@router.post("/me/notifications/read")
def mark_read(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Notification).filter_by(user_id=user.id, is_read=False).update({"is_read": True})
    db.commit()
    return {"ok": True}
