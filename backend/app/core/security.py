"""Session cookies and server-side authorisation (PRD §15, D3).

The UI never decides access: `require_roles` is the only way a route declares it.
"""

import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from fastapi import Depends, Request, Response
from sqlalchemy.orm import Session as DbSession

from app.core.config import get_settings
from app.core.errors import Forbidden, NotFound, Unauthorized
from app.db.session import get_db
from app.models import User, UserRole
from app.repositories import users as users_repo


@dataclass(frozen=True)
class Actor:
    id: uuid.UUID
    role: UserRole
    name: str

    def to_dict(self) -> dict[str, str]:
        return {"id": str(self.id), "role": self.role.value, "name": self.name}


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def issue_session(db: DbSession, user: User) -> str:
    """Create a session row and return the raw token (only its hash is stored)."""
    settings = get_settings()
    token = secrets.token_urlsafe(32)
    users_repo.add_session(
        db,
        user_id=user.id,
        token_hash=hash_token(token),
        expires_at=datetime.now(UTC) + timedelta(hours=settings.SESSION_TTL_HOURS),
    )
    return token


def revoke_session(db: DbSession, token: str) -> bool:
    row = users_repo.get_session_by_hash(db, hash_token(token))
    if row is None or row.revoked_at is not None:
        return False
    row.revoked_at = datetime.now(UTC)
    db.flush()
    return True


def set_session_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        settings.SESSION_COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.SESSION_TTL_HOURS * 3600,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(settings.SESSION_COOKIE_NAME, path="/")


def optional_actor(request: Request, db: DbSession = Depends(get_db)) -> Actor | None:
    token = request.cookies.get(get_settings().SESSION_COOKIE_NAME)
    if not token:
        return None
    row = users_repo.get_session_by_hash(db, hash_token(token))
    if row is None or row.revoked_at is not None:
        return None
    # Expiry is enforced here; the cookie Max-Age is a convenience only.
    if row.expires_at <= datetime.now(UTC):
        return None
    user = users_repo.get_by_id(db, row.user_id)
    if user is None:
        return None
    return Actor(id=user.id, role=UserRole(user.role), name=user.name)


def current_actor(actor: Actor | None = Depends(optional_actor)) -> Actor:
    if actor is None:
        raise Unauthorized()
    return actor


def require_demo_mode() -> None:
    """Gate demo-only routes.

    Declared as a route dependency, never called inside a handler: FastAPI solves
    decorator dependencies before parameter ones, so this runs ahead of
    `require_roles` and every caller gets the same 404 when demo mode is off. A
    401 or 403 would confirm the route exists (PRD §12).
    """
    if not get_settings().AWWAZ_DEMO_MODE:
        raise NotFound()


def require_roles(*roles: UserRole):  # type: ignore[no-untyped-def]
    allowed = set(roles)

    def _dependency(actor: Actor = Depends(current_actor)) -> Actor:
        if actor.role not in allowed:
            raise Forbidden()
        return actor

    return _dependency
