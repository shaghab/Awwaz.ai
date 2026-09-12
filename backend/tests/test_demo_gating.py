"""With AWWAZ_DEMO_MODE=false the demo endpoints must 404, not 403 (PRD §12)."""

import pytest

from .conftest import login


@pytest.fixture
def prod_mode(demo_mode):
    demo_mode(False)
    from fastapi.testclient import TestClient

    from app.main import create_app

    with TestClient(create_app()) as c:
        yield c


def test_demo_login_is_hidden(prod_mode):
    response = prod_mode.post("/api/v1/auth/demo-login", json={"user_key": "sara"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_demo_reset_is_hidden_even_for_admin(client, seeded, demo_mode):
    login(client, "bilal")
    demo_mode(False)
    assert client.post("/api/v1/admin/demo/reset").status_code == 404
