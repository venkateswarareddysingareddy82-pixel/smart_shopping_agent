"""Central configuration. All secrets come from environment variables / .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent

# Load .env from backend/ first, then project root (first one wins).
for _p in (BACKEND_DIR / ".env", PROJECT_DIR / ".env"):
    if _p.exists():
        load_dotenv(_p, override=False)


def env(name: str, default: str = "") -> str:
    """Return env var, treating empty strings as 'not set'."""
    value = os.getenv(name, "")
    return value.strip() if value and value.strip() else default


def _database_url() -> str:
    url = env("DATABASE_URL", f"sqlite:///{(BACKEND_DIR / 'smart_shopping.db').as_posix()}")
    if url.startswith("postgres://"):  # Render/Heroku style
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Settings:
    APP_NAME = "Smart Shopping Platform"
    DATABASE_URL = _database_url()
    SECRET_KEY = env("SECRET_KEY", "dev-only-secret-change-me-before-deploying")
    TOKEN_EXPIRE_MINUTES = int(env("TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days
    FRONTEND_URL = env("FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL = env("BACKEND_URL", "http://localhost:8000")
    # AI (optional – app works fully without it in demo mode)
    AI_API_KEY = env("AI_API_KEY")
    AI_PROVIDER = env("AI_PROVIDER", "anthropic").lower()  # anthropic | openai
    AI_MODEL = env("AI_MODEL", "claude-haiku-4-5-20251001")
    AI_BASE_URL = env("AI_BASE_URL")  # optional override (OpenAI-compatible servers)
    AI_TIMEOUT = float(env("AI_TIMEOUT", "30"))
    AUTO_SEED = env("AUTO_SEED", "true").lower() in ("1", "true", "yes")
    # Development-only demo credentials (override in .env)
    SEED_ADMIN_EMAIL = env("SEED_ADMIN_EMAIL", "admin@example.com")
    SEED_ADMIN_PASSWORD = env("SEED_ADMIN_PASSWORD", "Admin@12345")
    SEED_USER_EMAIL = env("SEED_USER_EMAIL", "user@example.com")
    SEED_USER_PASSWORD = env("SEED_USER_PASSWORD", "User@12345")

    @property
    def cors_origins(self) -> list[str]:
        origins = {self.FRONTEND_URL.rstrip("/"), "http://localhost:5173", "http://127.0.0.1:5173",
                   "http://localhost:3000", "http://localhost"}
        extra = env("CORS_ORIGINS")
        if extra:
            origins.update(o.strip().rstrip("/") for o in extra.split(",") if o.strip())
        return sorted(origins)

    @property
    def ai_enabled(self) -> bool:
        return bool(self.AI_API_KEY)


settings = Settings()
