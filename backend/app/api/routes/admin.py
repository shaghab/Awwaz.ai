"""Admin/demo operations (PRD §12: disabled in production)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.core.envelope import ok
from app.core.security import Actor, require_demo_mode, require_roles
from app.db.session import get_db
from app.domain.audit import service as audit
from app.models import ActorType, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/demo/reset", dependencies=[Depends(require_demo_mode)])
def demo_reset(
    actor: Actor = Depends(require_roles(UserRole.ADMIN)),
    db: DbSession = Depends(get_db),
) -> dict[str, object]:
    from app.seed import reset_demo_data

    counts = reset_demo_data(db)
    audit.record(
        db,
        actor_id=actor.id,
        actor_type=ActorType.USER,
        action="DEMO_RESET",
        resource_type="system",
        metadata=counts,
    )
    db.commit()
    return ok(counts)
