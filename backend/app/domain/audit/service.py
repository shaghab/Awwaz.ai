"""Audit sink used by every consequential mutation (PRD §13, A10)."""

import uuid
from typing import Any

from sqlalchemy.orm import Session as DbSession

from app.core.request_id import get_request_id
from app.models import ActorType, AuditLog, AuditResult
from app.repositories import audit as audit_repo


def record(
    db: DbSession,
    *,
    action: str,
    resource_type: str,
    actor_id: uuid.UUID | None = None,
    actor_type: ActorType = ActorType.USER,
    resource_id: str | None = None,
    request_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    result: AuditResult = AuditResult.SUCCESS,
) -> AuditLog:
    return audit_repo.add(
        db,
        actor_id=actor_id,
        actor_type=actor_type,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        request_id=request_id or get_request_id(),
        result=result,
        meta=metadata or {},
    )
