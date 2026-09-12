from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.security import hash_token
from app.models import Session

from .conftest import login

COOKIE = "awwaz_session"


def test_login_sets_httponly_cookie_and_returns_actor(client, seeded):
    response = login(client, "sara")
    assert response.json()["data"]["actor"]["role"] == "OPERATOR"
    cookie = response.headers["set-cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=lax" in cookie.replace("samesite", "SameSite")


def test_me_requires_a_session(client, seeded):
    assert client.get("/api/v1/auth/me").status_code == 401
    login(client, "hamza")
    body = client.get("/api/v1/auth/me").json()
    assert body["data"]["actor"]["name"] == "Hamza Iqbal"


def test_operator_cannot_use_an_admin_route(client, seeded):
    login(client, "sara")
    response = client.post("/api/v1/admin/demo/reset")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_admin_can_use_an_admin_route(client, seeded):
    login(client, "bilal")
    assert client.post("/api/v1/admin/demo/reset").status_code == 200


def test_revoked_session_is_unauthorized(client, seeded):
    login(client, "sara")
    assert client.post("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 401


def test_expired_session_is_unauthorized(client, seeded, db):
    login(client, "sara")
    token = client.cookies[COOKIE]
    row = db.scalar(select(Session).where(Session.token_hash == hash_token(token)))
    row.expires_at = datetime.now(UTC) - timedelta(minutes=1)
    db.commit()
    assert client.get("/api/v1/auth/me").status_code == 401


def test_unknown_demo_user_is_not_found(client, seeded):
    response = client.post("/api/v1/auth/demo-login", json={"user_key": "worker"})
    assert response.status_code == 404


def test_service_account_cannot_log_in(client, seeded):
    response = client.post("/api/v1/auth/demo-login", json={"user_key": "awwaz-worker"})
    assert response.status_code == 404


def test_only_the_token_hash_is_stored(client, seeded, db):
    login(client, "sara")
    token = client.cookies[COOKIE]
    hashes = list(db.scalars(select(Session.token_hash)))
    assert token not in hashes
    assert hash_token(token) in hashes
