from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.security import create_token, get_current_user, hash_password, verify_password
from ..database import get_db
from ..models import User
from ..schemas import LoginIn, RegisterIn
from ..ai.language import normalize_lang

router = APIRouter(prefix="/api/auth", tags=["auth"])


def user_dict(u: User) -> dict:
    return {"id": u.id, "name": u.name, "email": u.email, "phone": u.phone, "is_admin": u.is_admin,
            "preferred_language": u.preferred_language, "created_at": u.created_at.isoformat()}


@router.post("/register", status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "An account with this email already exists. Please log in.")
    u = User(name=data.name.strip(), email=email, password_hash=hash_password(data.password), phone=data.phone,
             preferred_language=normalize_lang(data.preferred_language))
    db.add(u)
    db.commit()
    return {"token": create_token(u), "user": user_dict(u)}


@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == data.email.lower()).first()
    if not u or not verify_password(data.password, u.password_hash):
        raise HTTPException(401, "Email or password is wrong. Please try again.")
    if not u.is_active:
        raise HTTPException(403, "This account is disabled. Please contact support.")
    return {"token": create_token(u), "user": user_dict(u)}


@router.post("/logout")
def logout(_: User = Depends(get_current_user)):
    # JWTs are stateless: the client discards the token. Endpoint exists for symmetry/audit.
    return {"ok": True}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user_dict(user)
