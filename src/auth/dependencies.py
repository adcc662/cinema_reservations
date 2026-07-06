"""FastAPI security wiring: extract the token, resolve the user, enforce roles.

This is the layer routers depend on. A protected endpoint just declares:

    @router.get("/me")
    def me(user: User = Depends(get_current_active_user)):
        ...

An admin-only endpoint declares:

    @router.post("/movies", dependencies=[Depends(require_admin)])
    def create_movie(...):
        ...
"""

import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.auth import security
from src.auth.schemas import TokenPayload
from src.auth.security import TokenType
from src.config import settings
from src.database.session import get_session
from src.roles.constants import RoleEnum
from src.users.models import User

# `tokenUrl` is only metadata for Swagger's "Authorize" button — it tells the
# docs where to POST credentials. Point it at the future login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Handy aliases so signatures stay readable.
SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """Decode the access token and load the matching user from the DB.

    We hit the database instead of trusting claims blindly so that a
    disabled account or a changed role takes effect immediately, not only
    when the token expires.
    """
    try:
        payload = security.decode_token(token, TokenType.ACCESS)
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise _credentials_exception

    if token_data.sub is None:
        raise _credentials_exception
    try:
        user_id = uuid.UUID(token_data.sub)
    except ValueError:
        raise _credentials_exception

    # Eager-load roles so the RBAC check below never triggers a lazy query.
    statement = (
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = session.exec(statement).first()
    if user is None:
        raise _credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_user(current_user: CurrentUser) -> User:
    """Reject users whose account has not been activated."""
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user


CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


class RoleChecker:
    """Dependency factory that enforces role-based access control.

    Grants access if the user has AT LEAST ONE of the allowed roles.
    Instantiate once, reuse everywhere:

        require_admin = RoleChecker(RoleEnum.ADMIN)
    """

    def __init__(self, *allowed_roles: RoleEnum) -> None:
        self.allowed_roles = {role.value for role in allowed_roles}

    def __call__(self, current_user: CurrentActiveUser) -> User:
        user_role_names = {role.name for role in current_user.roles}
        if self.allowed_roles.isdisjoint(user_role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user


# Ready-to-use guards.
require_admin = RoleChecker(RoleEnum.ADMIN)
require_user = RoleChecker(RoleEnum.USER, RoleEnum.ADMIN)
