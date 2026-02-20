from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict

from src.reservations.constants import ReservationStatus
from src.showtimes.schemas import Showtime
from src.users.schemas import User


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID4
    showtime_id: UUID4
    status: ReservationStatus = ReservationStatus.PENDING


class ReservationCreate(ReservationBase):
    user_id: UUID4
    showtime_id: UUID4
    seat_ids: List[UUID4]


class ReservationUpdate(ReservationBase):
    user_id: Optional[UUID4] = None
    showtime_id: Optional[UUID4] = None
    status: Optional[ReservationStatus] = None
    seat_ids: Optional[List[UUID4]] = None


class ReservationInDBBase(ReservationBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    user: Optional[User] = None
    showtime: Optional[Showtime] = None
    seat_ids: List[UUID4] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Reservation(ReservationInDBBase):
    pass


class ReservationInDB(ReservationInDBBase):
    pass
