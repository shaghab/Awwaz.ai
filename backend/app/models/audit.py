import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, created_at_column, uuid_pk


class ActorType(StrEnum):
    USER = "USER"
    AGENT = "AGENT"
    WORKER = "WORKER"
    SYSTEM = "SYSTEM"


class AuditResult(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class AuditLog(Base):
    """Append-only record of consequential actions (PRD §13, A10)."""

    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_resource", "resource_type", "resource_id"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    actor_id: Mapped[uuid.UUID | None] = mapped_column(PgUUID(as_uuid=True), nullable=True)
    actor_type: Mapped[ActorType] = mapped_column(String(20), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    request_id: Mapped[str] = mapped_column(String(128), nullable=False)
    result: Mapped[AuditResult] = mapped_column(String(20), nullable=False)
    meta: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = created_at_column()
