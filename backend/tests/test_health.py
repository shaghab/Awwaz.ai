from sqlalchemy.exc import OperationalError


def test_health_is_public(client):
    assert client.get("/health").status_code == 200


def test_ready_checks_the_database(client):
    body = client.get("/ready").json()
    assert body["data"] == {"status": "ready", "database": "ok"}


def test_ready_is_503_when_the_database_is_down(client, monkeypatch):
    from app.api.routes import health

    def _boom(*_args, **_kwargs):
        raise OperationalError("SELECT 1", {}, Exception("down"))

    monkeypatch.setattr(health.DbSession, "execute", _boom, raising=False)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "EXTERNAL_SERVICE_UNAVAILABLE"


def _app_that_raises(monkeypatch):
    from fastapi.testclient import TestClient

    from app.api.routes import health
    from app.main import create_app

    monkeypatch.setattr(health, "ok", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("boom")))
    return TestClient(create_app(), raise_server_exceptions=False)


def test_unhandled_exception_becomes_internal_error(test_database, monkeypatch):
    with _app_that_raises(monkeypatch) as c:
        response = c.get("/health")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert "boom" not in body["error"]["message"]


def test_unhandled_500_still_carries_the_request_id_header(test_database, monkeypatch):
    """Starlette's ServerErrorMiddleware builds its 500 outside the user
    middleware stack, so a response it creates is decorated by none of it."""
    with _app_that_raises(monkeypatch) as c:
        response = c.get("/health", headers={"X-Request-ID": "req_five_hundred"})
    assert response.headers.get("X-Request-ID") == "req_five_hundred"
    assert response.json()["error"]["request_id"] == "req_five_hundred"


def test_unhandled_500_is_readable_cross_origin(test_database, monkeypatch):
    """Without CORS headers the browser cannot read the body at all, so the
    truthful error envelope never reaches the user (PRD principle 3)."""
    origin = "http://localhost:3000"
    with _app_that_raises(monkeypatch) as c:
        response = c.get("/health", headers={"Origin": origin})
    assert response.status_code == 500
    assert response.headers.get("Access-Control-Allow-Origin") == origin


def test_ordinary_responses_keep_their_headers_cross_origin(client):
    origin = "http://localhost:3000"
    for path, expected in (("/health", 200), ("/api/v1/auth/me", 401)):
        response = client.get(path, headers={"Origin": origin})
        assert response.status_code == expected
        assert response.headers.get("Access-Control-Allow-Origin") == origin
        assert response.headers.get("X-Request-ID", "").startswith("req_")
