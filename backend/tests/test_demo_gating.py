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


def test_demo_reset_is_hidden_from_anonymous_callers(prod_mode):
    """The gate must beat the role dependency: a 401 here would confirm the route
    exists, which is exactly what demo mode being off is meant to hide."""
    assert prod_mode.post("/api/v1/admin/demo/reset").status_code == 404


def test_demo_reset_is_hidden_from_the_wrong_role(client, seeded, demo_mode):
    """Likewise a 403 — so sign in while demo mode is on, then turn it off."""
    login(client, "sara")
    demo_mode(False)
    assert client.post("/api/v1/admin/demo/reset").status_code == 404


def test_demo_users_is_hidden(prod_mode):
    assert prod_mode.get("/api/v1/auth/demo-users").status_code == 404


DEMO_PATHS = [
    ("POST", "/api/v1/auth/demo-login"),
    ("GET", "/api/v1/auth/demo-users"),
    ("POST", "/api/v1/admin/demo/reset"),
]


@pytest.mark.parametrize(("method", "path"), DEMO_PATHS)
def test_demo_routes_do_not_exist_at_all_in_prod_mode(prod_mode, method, path):
    """A wrong verb must not out them either: a registered route answers an
    undeclared method with 405 during routing, before dependencies run, which
    confirms it exists. An unmounted route is 404 for every verb."""
    assert prod_mode.request(method, path).status_code == 404

    wrong_verb = "GET" if method == "POST" else "DELETE"
    assert prod_mode.request(wrong_verb, path).status_code == 404


@pytest.mark.parametrize(("method", "path"), DEMO_PATHS)
def test_demo_routes_are_mounted_when_demo_mode_is_on(client, seeded, method, path):
    assert client.request(method, path).status_code != 404
