from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from src.auditoriums.schemas import Auditorium
from src.movies.schemas import Movie
from src.showtimes.constants import ShowtimeStatus


class ShowtimeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    movie_id: UUID4
    auditorium_id: UUID4
    starts_at: datetime
    price: Decimal
    status: ShowtimeStatus = ShowtimeStatus.SCHEDULED


class ShowtimeCreate(ShowtimeBase):
    movie_id: UUID4
    auditorium_id: UUID4
    starts_at: datetime
    price: Decimal


class ShowtimeUpdate(ShowtimeBase):
    movie_id: Optional[UUID4] = None
    auditorium_id: Optional[UUID4] = None
    starts_at: Optional[datetime] = None
    price: Optional[Decimal] = None
    status: Optional[ShowtimeStatus] = None


class ShowtimeInDBBase(ShowtimeBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    movie: Optional[Movie] = None
    auditorium: Optional[Auditorium] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Showtime(ShowtimeInDBBase):
    pass


class ShowtimeInDB(ShowtimeInDBBase):
    pass
