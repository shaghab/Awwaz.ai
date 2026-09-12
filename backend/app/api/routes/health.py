"""Liveness and readiness (PRD §23)."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.orm import Session as DbSession

from app.core.envelope import ok
from app.core.errors import ExternalServiceUnavailable
from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, object]:
    return ok({"status": "ok"})


@router.get("/ready")
def ready(response: Response, db: DbSession = Depends(get_db)) -> dict[str, object]:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - surfaced truthfully as 503
        raise ExternalServiceUnavailable("Database is not reachable.") from exc
    return ok({"status": "ready", "database": "ok"})
