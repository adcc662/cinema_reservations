import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.utils.utils import get_time_zone

if TYPE_CHECKING:
    from src.users.models import User

tz = pytz.timezone(get_time_zone())


class UserRoles(SQLModel, table=True):
    __tablename__ = "user_roles"
    role_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )
    user_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )


class Role(Base, SQLModel, table=True):
    __tablename__ = "roles"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRoles)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
