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


def test_unhandled_exception_becomes_internal_error(test_database, monkeypatch):
    from fastapi.testclient import TestClient

    from app.api.routes import health
    from app.main import create_app

    monkeypatch.setattr(health, "ok", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("boom")))
    with TestClient(create_app(), raise_server_exceptions=False) as c:
        response = c.get("/health")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert "boom" not in body["error"]["message"]
