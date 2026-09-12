from sqlalchemy import select

from app.models import User
from app.seed import seed_all


def test_seed_creates_four_users_and_is_idempotent(db):
    assert seed_all(db)["users_created"] == 4
    db.commit()
    assert seed_all(db)["users_created"] == 0
    db.commit()
    roles = sorted(db.scalars(select(User.role)))
    assert roles == ["ADMIN", "CITIZEN", "OPERATOR", "SERVICE"]
