from sqlalchemy import select

from app.models import AuditLog

from .conftest import login


def test_login_writes_exactly_one_audit_row(client, seeded, db):
    login(
        client,
        "sara",
    )
    rows = list(db.scalars(select(AuditLog).where(AuditLog.action == "AUTH_LOGIN")))
    assert len(rows) == 1
    row = rows[0]
    assert row.actor_id is not None
    assert row.actor_type == "USER"
    assert row.resource_type == "user"
    assert row.request_id.startswith("req_")
    assert row.result == "SUCCESS"
    assert row.meta["role"] == "OPERATOR"


def test_logout_is_audited(client, seeded, db):
    login(client, "sara")
    client.post("/api/v1/auth/logout")
    actions = list(db.scalars(select(AuditLog.action).order_by(AuditLog.created_at)))
    assert actions == ["AUTH_LOGIN", "AUTH_LOGOUT"]


def test_audit_row_uses_the_caller_request_id(client, seeded, db):
    client.post(
        "/api/v1/auth/demo-login",
        json={"user_key": "sara"},
        headers={"X-Request-ID": "req_trace_me"},
    )
    row = db.scalar(select(AuditLog))
    assert row.request_id == "req_trace_me"
