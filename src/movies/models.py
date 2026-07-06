import uuid as uuid_pkg
from datetime import date, datetime
from typing import TYPE_CHECKING

import pytz
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import Base
from src.utils.utils import get_time_zone, updated_at_column

if TYPE_CHECKING:
    from src.showtimes.models import Showtime

tz = pytz.timezone(get_time_zone())


class MovieGenres(SQLModel, table=True):
    __tablename__ = "movie_genres"
    movie_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="movies.id", primary_key=True
    )
    genre_id: uuid_pkg.UUID | None = Field(
        default=None, foreign_key="genres.id", primary_key=True
    )


class Genre(Base, SQLModel, table=True):
    __tablename__ = "genres"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(index=True, unique=True, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(sa_column=updated_at_column())
    movies: list["Movie"] = Relationship(
        back_populates="genres", link_model=MovieGenres
    )


class Movie(Base, SQLModel, table=True):
    __tablename__ = "movies"
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    poster_url: str | None = Field(default=None, nullable=True)
    duration_minutes: int = Field(nullable=False)
    release_date: date = Field(nullable=False)
    rating: str | None = Field(default=None, nullable=True)
    director: str | None = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz), nullable=False
    )
    updated_at: datetime = Field(sa_column=updated_at_column())
    genres: list["Genre"] = Relationship(
        back_populates="movies", link_model=MovieGenres
    )
    showtimes: list["Showtime"] = Relationship(back_populates="movie")
