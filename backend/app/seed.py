"""Idempotent seed entrypoint: `python -m app.seed` (upserts by natural key)."""

import logging

from sqlalchemy import delete
from sqlalchemy.orm import Session as DbSession

from app.core.logging import configure_logging
from app.db.session import SessionLocal
from app.domain.users.service import DEMO_USERS
from app.models import User, UserRole
from app.repositories import users as users_repo

logger = logging.getLogger("awwaz.seed")

# Truncated by `POST /admin/demo/reset`, newest-dependency first. Slice 2+ append here.
DEMO_DATA_TABLES: list[type] = []


def seed_users(db: DbSession) -> int:
    created = 0
    for spec in DEMO_USERS:
        existing = users_repo.get_by_demo_key(db, spec["demo_key"])
        if existing is None:
            db.add(
                User(
                    name=spec["name"],
                    email=spec["email"],
                    role=UserRole(spec["role"]),
                    demo_key=spec["demo_key"],
                )
            )
            created += 1
        else:
            existing.name = spec["name"]
            existing.email = spec["email"]
            existing.role = UserRole(spec["role"])
    db.flush()
    return created


def seed_all(db: DbSession) -> dict[str, int]:
    return {"users_created": seed_users(db)}


def reset_demo_data(db: DbSession) -> dict[str, int]:
    """Clear domain data and re-run the seed. Users and sessions survive so the
    admin performing the reset is not logged out."""
    for model in DEMO_DATA_TABLES:
        db.execute(delete(model))
    db.flush()
    return seed_all(db)


def main() -> None:
    configure_logging()
    with SessionLocal() as db:
        counts = seed_all(db)
        db.commit()
    logger.info("seed_complete", extra={"route": "seed", **counts})
    print(f"Seed complete: {counts}")


if __name__ == "__main__":
    main()
