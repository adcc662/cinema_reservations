import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.reservations.constants import ReservationStatus
from src.utils.utils import get_time_zone

if TYPE_CHECKING:
    from src.auditoriums.models import Seat
    from src.showtimes.models import Showtime
    from src.users.models import User

tz = pytz.timezone(get_time_zone())


class ReservationSeats(SQLModel, table=True):
    __tablename__ = "reservation_seats"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    reservation_id: uuid_pkg.UUID = Field(foreign_key="reservations.id", nullable=False)
    seat_id: uuid_pkg.UUID = Field(foreign_key="seats.id", nullable=False)
    showtime_id: uuid_pkg.UUID = Field(foreign_key="showtimes.id", nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )


class Reservation(Base, SQLModel, table=True):
    __tablename__ = "reservations"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    user_id: uuid_pkg.UUID = Field(foreign_key="users.id", nullable=False)
    showtime_id: uuid_pkg.UUID = Field(foreign_key="showtimes.id", nullable=False)
    status: str = Field(default=ReservationStatus.PENDING.value, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    user: "User" = Relationship(back_populates="reservations")
    showtime: "Showtime" = Relationship(back_populates="reservations")
    seats: list["Seat"] = Relationship(link_model=ReservationSeats)
