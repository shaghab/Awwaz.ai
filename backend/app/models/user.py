import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, created_at_column, updated_at_column, uuid_pk


class UserRole(StrEnum):
    CITIZEN = "CITIZEN"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320), unique=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False)
    demo_key: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
