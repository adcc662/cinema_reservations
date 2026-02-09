import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.roles.models import UserRoles
from src.utils.utils import get_time_zone

if TYPE_CHECKING:
    from src.reservations.models import Reservation
    from src.roles.models import Role

tz = pytz.timezone(get_time_zone())


class User(Base, SQLModel, table=True):
    __tablename__ = "users"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(nullable=False)
    email: str = Field(index=True, unique=True)
    hashed_password: str = Field(nullable=False)
    active: bool = Field(default=False)
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRoles)
    reservations: list["Reservation"] = Relationship(back_populates="user")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
