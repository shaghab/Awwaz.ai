"""Demo authentication (PRD §15, D3)."""

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession

from app.core.config import get_settings
from app.core.envelope import ok
from app.core.security import (
    Actor,
    clear_session_cookie,
    current_actor,
    require_demo_mode,
    set_session_cookie,
)
from app.db.session import get_db
from app.domain.audit import service as audit
from app.domain.users import service as users
from app.models import ActorType, AuditResult

router = APIRouter(prefix="/auth", tags=["auth"])


class DemoLoginRequest(BaseModel):
    user_key: str


@router.post("/demo-login", dependencies=[Depends(require_demo_mode)])
def demo_login(
    payload: DemoLoginRequest, response: Response, db: DbSession = Depends(get_db)
) -> dict[str, object]:
    actor, token = users.login_demo_user(db, payload.user_key)
    audit.record(
        db,
        actor_id=actor.id,
        actor_type=ActorType.USER,
        action="AUTH_LOGIN",
        resource_type="user",
        resource_id=str(actor.id),
        metadata={"demo_key": payload.user_key, "role": actor.role.value},
        result=AuditResult.SUCCESS,
    )
    db.commit()
    set_session_cookie(response, token)
    return ok({"actor": actor.to_dict()})


@router.get("/demo-users", dependencies=[Depends(require_demo_mode)])
def demo_users(db: DbSession = Depends(get_db)) -> dict[str, object]:
    return ok(
        {
            "users": [
                {"user_key": u.demo_key, "name": u.name, "role": u.role}
                for u in users.get_demo_users(db)
                if u.demo_key in users.LOGIN_KEYS
            ]
        }
    )


@router.get("/me")
def me(actor: Actor = Depends(current_actor)) -> dict[str, object]:
    return ok({"actor": actor.to_dict()})


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    actor: Actor = Depends(current_actor),
    db: DbSession = Depends(get_db),
) -> dict[str, object]:
    token = request.cookies.get(get_settings().SESSION_COOKIE_NAME)
    revoked = users.logout(db, token)
    audit.record(
        db,
        actor_id=actor.id,
        actor_type=ActorType.USER,
        action="AUTH_LOGOUT",
        resource_type="user",
        resource_id=str(actor.id),
        result=AuditResult.SUCCESS if revoked else AuditResult.FAILURE,
    )
    db.commit()
    clear_session_cookie(response)
    return ok({"logged_out": True})
