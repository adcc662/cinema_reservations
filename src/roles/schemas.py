from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict


# --- UserRoles schemas ---
class UserRolesBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_id: UUID4
    user_id: UUID4


class UserRolesCreate(UserRolesBase):
    role_id: UUID4
    user_id: UUID4


class UserRolesUpdate(UserRolesBase):
    role_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None


class UserRolesInDBBase(UserRolesBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: Optional[datetime] = None


class UserRoles(UserRolesInDBBase):
    pass


class UserRolesInDB(UserRolesInDBBase):
    pass


# --- Role schemas ---
class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str


class RoleCreate(RoleBase):
    name: str
    description: str


class RoleUpdate(RoleBase):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleInDBBase(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass
