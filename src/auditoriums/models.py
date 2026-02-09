import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.utils.utils import get_time_zone

if TYPE_CHECKING:
    from src.showtimes.models import Showtime

tz = pytz.timezone(get_time_zone())


class Seat(Base, SQLModel, table=True):
    __tablename__ = "seats"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    auditorium_id: uuid_pkg.UUID = Field(foreign_key="auditoriums.id", nullable=False)
    seat_number: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    auditorium: "Auditorium" = Relationship(back_populates="seats")


class Auditorium(Base, SQLModel, table=True):
    __tablename__ = "auditoriums"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(index=True, unique=True, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    seats: list["Seat"] = Relationship(back_populates="auditorium")
    showtimes: list["Showtime"] = Relationship(back_populates="auditorium")
