import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import User

_ITER = 200_000
_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _ITER).hex()
    return f"pbkdf2_sha256${_ITER}${salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, iters, salt, digest = stored.split("$")
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iters)).hex()
        return hmac.compare_digest(check, digest)
    except Exception:
        return False


def create_token(user: User) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user.id), "admin": user.is_admin, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")


def _user_from_creds(creds, db: Session):
    if not creds:
        return None
    try:
        payload = jwt.decode(creds.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        user = db.get(User, int(payload["sub"]))
    except Exception:
        return None
    return user if user and user.is_active else None


def get_optional_user(creds: HTTPAuthorizationCredentials = Depends(_bearer), db: Session = Depends(get_db)):
    return _user_from_creds(creds, db)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(_bearer), db: Session = Depends(get_db)) -> User:
    user = _user_from_creds(creds, db)
    if not user:
        raise HTTPException(401, "Please log in to continue.")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Only administrators can do this.")
    return user
