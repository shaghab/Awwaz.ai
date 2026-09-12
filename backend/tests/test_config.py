"""The documented quick start creates `.env` at the repository root, but every
backend command runs from `backend/`. A relative env_file would silently miss it.
"""

from pathlib import Path

from app.core.config import Settings


def test_settings_read_the_repo_root_env_file():
    env_file = Settings.model_config["env_file"]
    assert env_file is not None
    root = Path(str(env_file)).parent
    assert Path(str(env_file)).name == ".env"
    # The repository root is the directory holding .env.example and the Makefile.
    assert (root / ".env.example").is_file()
    assert (root / "Makefile").is_file()


def test_demo_mode_is_refused_in_production():
    """Together these two settings are a passwordless ADMIN login (Codex P1)."""
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError, match="AWWAZ_DEMO_MODE must be false"):
        Settings(
            DATABASE_URL="postgresql+psycopg://x@localhost/x",
            AUTH_SECRET="x",
            AWWAZ_ENV="prod",
            AWWAZ_DEMO_MODE=True,
        )


def test_production_without_demo_mode_is_fine():
    settings = Settings(
        DATABASE_URL="postgresql+psycopg://x@localhost/x",
        AUTH_SECRET="x",
        AWWAZ_ENV="prod",
        AWWAZ_DEMO_MODE=False,
    )
    assert settings.cookie_secure is True


def test_demo_mode_outside_production_is_fine():
    settings = Settings(
        DATABASE_URL="postgresql+psycopg://x@localhost/x",
        AUTH_SECRET="x",
        AWWAZ_ENV="dev",
        AWWAZ_DEMO_MODE=True,
    )
    assert settings.AWWAZ_DEMO_MODE is True
