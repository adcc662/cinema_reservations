from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict


# --- Seat schemas ---
class SeatBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    seat_number: str
    auditorium_id: UUID4


class SeatCreate(SeatBase):
    ...


class SeatUpdate(SeatBase):
    seat_number: Optional[str] = None
    auditorium_id: Optional[UUID4] = None


class SeatInDBBase(SeatBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Seat(SeatInDBBase):
    pass


class SeatInDB(SeatInDBBase):
    pass


# --- Auditorium schemas ---
class AuditoriumBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class AuditoriumCreate(AuditoriumBase):
    ...


class AuditoriumUpdate(AuditoriumBase):
    name: Optional[str] = None


class AuditoriumInDBBase(AuditoriumBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    seats: List[Seat] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Auditorium(AuditoriumInDBBase):
    pass


class AuditoriumInDB(AuditoriumInDBBase):
    pass
