from datetime import datetime
from typing import List, Optional, Union

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr

from src.roles.schemas import Role


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: Optional[EmailStr] = None
    active: Optional[bool] = False


class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: Union[str, None]


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    roles: List[Role] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class Msg(BaseModel):
    msg: str
