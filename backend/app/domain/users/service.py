"""Demo persona lookup and session lifecycle (D3)."""

from sqlalchemy.orm import Session as DbSession

from app.core.errors import NotFound
from app.core.security import Actor, issue_session, revoke_session
from app.models import User, UserRole
from app.repositories import users as users_repo

DEMO_USERS: list[dict[str, str]] = [
    {"demo_key": "hamza", "name": "Hamza Iqbal", "email": "hamza@awwaz.demo", "role": "CITIZEN"},
    {"demo_key": "sara", "name": "Sara Khan", "email": "sara@awwaz.demo", "role": "OPERATOR"},
    {"demo_key": "bilal", "name": "Bilal Ahmed", "email": "bilal@awwaz.demo", "role": "ADMIN"},
    {
        "demo_key": "awwaz-worker",
        "name": "Awwaz Worker",
        "email": "worker@awwaz.demo",
        "role": "SERVICE",
    },
]

# Personas offered on the login screen; the SERVICE account is not one of them.
LOGIN_KEYS = ("hamza", "sara", "bilal")


def get_demo_users(db: DbSession) -> list[User]:
    return users_repo.list_demo_users(db)


def login_demo_user(db: DbSession, user_key: str) -> tuple[Actor, str]:
    if user_key not in LOGIN_KEYS:
        raise NotFound("Unknown demo user.")
    user = users_repo.get_by_demo_key(db, user_key)
    if user is None:
        raise NotFound("Demo user is not seeded. Run `make seed`.")
    token = issue_session(db, user)
    return Actor(id=user.id, role=UserRole(user.role), name=user.name), token


def logout(db: DbSession, token: str | None) -> bool:
    return revoke_session(db, token) if token else False
