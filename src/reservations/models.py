import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.reservations.constants import ReservationStatus
from src.utils.utils import get_time_zone, updated_at_column

if TYPE_CHECKING:
    from src.auditoriums.models import Seat
    from src.showtimes.models import Showtime
    from src.users.models import User

tz = pytz.timezone(get_time_zone())


class ReservationSeats(SQLModel, table=True):
    __tablename__ = "reservation_seats"
    reservation_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="reservations.id", primary_key=True
    )
    seat_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="seats.id", primary_key=True
    )
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
    updated_at: datetime = Field(sa_column=updated_at_column())
    user: "User" = Relationship(back_populates="reservations")
    showtime: "Showtime" = Relationship(back_populates="reservations")
    seats: list["Seat"] = Relationship(link_model=ReservationSeats)
