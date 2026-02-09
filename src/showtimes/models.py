import uuid as uuid_pkg
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.showtimes.constants import ShowtimeStatus
from src.utils.utils import get_time_zone

if TYPE_CHECKING:
    from src.auditoriums.models import Auditorium
    from src.movies.models import Movie
    from src.reservations.models import Reservation

tz = pytz.timezone(get_time_zone())


class Showtime(Base, SQLModel, table=True):
    __tablename__ = "showtimes"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    movie_id: uuid_pkg.UUID = Field(foreign_key="movies.id", nullable=False)
    auditorium_id: uuid_pkg.UUID = Field(foreign_key="auditoriums.id", nullable=False)
    starts_at: datetime = Field(nullable=False)
    duration_minutes: int = Field(nullable=False)
    price: Decimal = Field(max_digits=10, decimal_places=2, nullable=False)
    status: str = Field(default=ShowtimeStatus.SCHEDULED.value, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    movie: "Movie" = Relationship(back_populates="showtimes")
    auditorium: "Auditorium" = Relationship(back_populates="showtimes")
    reservations: list["Reservation"] = Relationship(back_populates="showtime")
