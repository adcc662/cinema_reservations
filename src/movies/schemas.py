from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict


# --- Genre schemas ---
class GenreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class GenreCreate(GenreBase):
    ...


class GenreUpdate(GenreBase):
    name: Optional[str] = None


class GenreInDBBase(GenreBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Genre(GenreInDBBase):
    pass


class GenreInDB(GenreInDBBase):
    pass


# --- Movie schemas ---
class MovieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    poster_url: Optional[str] = None
    duration_minutes: int
    release_date: date
    rating: Optional[str] = None
    director: Optional[str] = None


class MovieCreate(MovieBase):
    genre_ids: Optional[List[UUID4]] = []


class MovieUpdate(MovieBase):
    name: Optional[str] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    release_date: Optional[date] = None
    rating: Optional[str] = None
    director: Optional[str] = None
    genre_ids: Optional[List[UUID4]] = None


class MovieInDBBase(MovieBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    genres: List[Genre] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Movie(MovieInDBBase):
    pass


class MovieInDB(MovieInDBBase):
    pass
