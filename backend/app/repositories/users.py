"""Persistence only, no policy (PRD §11)."""

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.models import Session, User


def get_by_demo_key(db: DbSession, demo_key: str) -> User | None:
    return db.scalar(select(User).where(User.demo_key == demo_key))


def get_by_id(db: DbSession, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def list_demo_users(db: DbSession) -> list[User]:
    return list(db.scalars(select(User).where(User.demo_key.is_not(None)).order_by(User.name)))


def add_session(
    db: DbSession, *, user_id: uuid.UUID, token_hash: str, expires_at: datetime
) -> Session:
    row = Session(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    db.add(row)
    db.flush()
    return row


def get_session_by_hash(db: DbSession, token_hash: str) -> Session | None:
    return db.scalar(select(Session).where(Session.token_hash == token_hash))
