from app.core.request_id import HEADER


def test_incoming_request_id_is_echoed(client):
    response = client.get("/health", headers={HEADER: "req_from_client"})
    assert response.headers[HEADER] == "req_from_client"
    assert response.json()["meta"]["request_id"] == "req_from_client"


def test_request_id_is_generated_when_absent(client):
    response = client.get("/health")
    assert response.headers[HEADER].startswith("req_")


def test_error_responses_carry_the_request_id(client):
    response = client.get("/api/v1/auth/me", headers={HEADER: "req_err"})
    assert response.json()["error"]["request_id"] == "req_err"
    assert response.headers[HEADER] == "req_err"
