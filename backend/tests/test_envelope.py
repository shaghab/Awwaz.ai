"""Success and error envelopes must match PRD §12 exactly."""


def test_success_envelope(client):
    body = client.get("/health").json()
    assert body["success"] is True
    assert body["data"] == {"status": "ok"}
    assert body["meta"]["request_id"].startswith("req_")


def test_error_envelope(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert body["error"]["message"]
    assert body["error"]["request_id"].startswith("req_")
    assert "data" not in body


def test_validation_error_envelope(client):
    response = client.post("/api/v1/auth/demo-login", json={})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_unknown_route_is_not_found(client):
    response = client.get("/api/v1/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
