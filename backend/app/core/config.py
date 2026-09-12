"""Application settings (PRD §27)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# The Makefile runs every backend command from `backend/`, so a relative env_file
# would resolve there. The documented quick start creates `.env` at the
# repository root, which is what this points at.
REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    # Required (PRD §27)
    DATABASE_URL: str
    APP_BASE_URL: str = "http://localhost:3000"
    BACKEND_BASE_URL: str = "http://localhost:8000"
    AUTH_SECRET: str

    # Flags
    AWWAZ_ENV: Literal["dev", "test", "prod"] = "dev"
    AWWAZ_DEMO_MODE: bool = False

    SESSION_TTL_HOURS: int = 12
    SESSION_COOKIE_NAME: str = "awwaz_session"

    @property
    def cookie_secure(self) -> bool:
        return self.AWWAZ_ENV == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
