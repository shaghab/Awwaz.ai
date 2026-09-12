"""Production must not publish the generated schema: it lists the demo routes
that the 404 gating exists to conceal (Codex P2)."""

import pytest
from fastapi.testclient import TestClient

DOC_PATHS = ["/docs", "/redoc", "/openapi.json"]


@pytest.fixture
def app_in(test_database, monkeypatch):
    def _build(env: str):
        from app.core.config import get_settings

        get_settings.cache_clear()
        monkeypatch.setenv("AWWAZ_ENV", env)
        if env == "prod":
            monkeypatch.setenv("AWWAZ_DEMO_MODE", "false")
        get_settings.cache_clear()

        from app.main import create_app

        return TestClient(create_app())

    yield _build
    from app.core.config import get_settings

    get_settings.cache_clear()


@pytest.mark.parametrize("path", DOC_PATHS)
def test_docs_are_not_published_in_production(app_in, path):
    with app_in("prod") as client:
        assert client.get(path).status_code == 404


@pytest.mark.parametrize("path", DOC_PATHS)
def test_docs_are_available_outside_production(app_in, path):
    with app_in("dev") as client:
        assert client.get(path).status_code == 200


def test_production_schema_cannot_leak_demo_routes(app_in):
    with app_in("prod") as client:
        assert client.get("/openapi.json").status_code == 404
