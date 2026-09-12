"""Application settings (PRD §27)."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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
