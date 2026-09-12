"""Persistence only, no policy (PRD §11)."""

from typing import Any

from sqlalchemy.orm import Session as DbSession

from app.models import AuditLog


def add(db: DbSession, **fields: Any) -> AuditLog:
    row = AuditLog(**fields)
    db.add(row)
    db.flush()
    return row
