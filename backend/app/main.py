import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .api import admin, ai_routes, auth, cart, orders, products, reviews, users
from .config import settings
from .database import Base, SessionLocal, engine
from .seed import seed
from .services.products import refresh_group_cache

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = FastAPI(title=settings.APP_NAME, version="1.0.0", description="AI voice-shopping e-commerce API")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

for r in (auth, users, products, cart, orders, reviews, ai_routes, admin):
    app.include_router(r.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    if settings.AUTO_SEED:
        try:
            if seed():
                log.info("Seeded demo data.")
        except Exception:
            log.exception("Seeding failed")
    db = SessionLocal()
    try:
        refresh_group_cache(db)
    finally:
        db.close()
    if settings.SECRET_KEY.startswith("dev-only"):
        log.warning("SECRET_KEY is the development default. Set a strong SECRET_KEY in .env before deploying.")
    log.info("AI mode: %s", "AI API enabled" if settings.ai_enabled else "demo mode (no AI_API_KEY)")


@app.get("/api/health")
def health():
    db_ok = True
    try:
        with engine.connect() as c:
            c.execute(text("select 1"))
    except Exception:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "database": db_ok, "ai_enabled": settings.ai_enabled}


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(x) for x in first.get("loc", [])[1:]) or "input"
    return JSONResponse(status_code=422, content={"detail": f"Please check '{field}': {first.get('msg', 'invalid value')}."})


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": "Something went wrong on our side. Please try again in a moment."})
