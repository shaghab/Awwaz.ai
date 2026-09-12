"""Tests run against a throwaway PostgreSQL database (D2), created once per session.

The database and its environment are set up at import time: test modules import
``app.*`` at collection, and ``app.db.session`` builds its engine on import.
"""

import os
import uuid

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url

ADMIN_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://postgres@localhost:5432/postgres"
)
_DB_NAME = f"awwaz_test_{uuid.uuid4().hex[:12]}"
_admin = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")

with _admin.connect() as _conn:
    _conn.execute(text(f'CREATE DATABASE "{_DB_NAME}"'))

os.environ["DATABASE_URL"] = (
    make_url(ADMIN_URL).set(database=_DB_NAME).render_as_string(hide_password=False)
)
os.environ["AUTH_SECRET"] = "test-secret"
os.environ["AWWAZ_ENV"] = "test"
os.environ["AWWAZ_DEMO_MODE"] = "true"


@pytest.fixture(scope="session", autouse=True)
def test_database():
    from alembic.config import Config

    from alembic import command

    command.upgrade(Config("alembic.ini"), "head")

    yield os.environ["DATABASE_URL"]

    from app.db.session import engine

    engine.dispose()
    with _admin.connect() as conn:
        conn.execute(
            text(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                f"WHERE datname = '{_DB_NAME}'"
            )
        )
        conn.execute(text(f'DROP DATABASE IF EXISTS "{_DB_NAME}"'))
    _admin.dispose()


@pytest.fixture
def db(test_database):
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def clean_tables(test_database):
    from app.db.session import engine

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE audit_logs, sessions, users RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def seeded(test_database):
    from app.db.session import SessionLocal
    from app.seed import seed_all

    with SessionLocal() as session:
        seed_all(session)
        session.commit()


@pytest.fixture
def client(test_database):
    from fastapi.testclient import TestClient

    from app.main import create_app

    with TestClient(create_app()) as c:
        yield c


@pytest.fixture
def demo_mode(monkeypatch):
    """Flip AWWAZ_DEMO_MODE for a single test (settings are cached)."""

    def _set(enabled: bool):
        from app.core.config import get_settings

        get_settings.cache_clear()
        monkeypatch.setenv("AWWAZ_DEMO_MODE", "true" if enabled else "false")
        get_settings.cache_clear()
        return get_settings()

    yield _set
    from app.core.config import get_settings

    get_settings.cache_clear()


def login(client, user_key: str = "sara"):
    response = client.post("/api/v1/auth/demo-login", json={"user_key": user_key})
    assert response.status_code == 200, response.text
    return response
