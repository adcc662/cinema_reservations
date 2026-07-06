"""Low-level security primitives: password hashing and JWT handling.

Nothing here touches the database or FastAPI — these are pure functions so
they're trivial to unit test. The web wiring lives in dependencies.py.
"""

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional, Union

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from src.config import settings

# Hash with bcrypt (handles salting for us). pwdlib.PasswordHash can hold
# several hashers: the first is used for new hashes, the rest let you verify
# (and transparently migrate) older hashes if you change algorithm later.
_password_hash = PasswordHash((BcryptHasher(),))


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


# --- Passwords ---------------------------------------------------------------


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage in User.hashed_password."""
    return _password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt against the stored hash. Constant-time."""
    return _password_hash.verify(plain_password, hashed_password)


# --- JSON Web Tokens ---------------------------------------------------------


def _create_token(
    subject: Union[str, Any],
    secret_key: str,
    expires_minutes: int,
    token_type: TokenType,
    additional_claims: Optional[dict[str, Any]] = None,
) -> str:
    """Build and sign a JWT.

    The refresh token is signed with a DIFFERENT secret than the access
    token. That way, leaking one signing key does not compromise the other.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": token_type.value,
    }
    if additional_claims:
        payload.update(additional_claims)
    return jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)


def create_access_token(
    subject: Union[str, Any],
    additional_claims: Optional[dict[str, Any]] = None,
) -> str:
    return _create_token(
        subject,
        secret_key=settings.JWT_SECRET_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type=TokenType.ACCESS,
        additional_claims=additional_claims,
    )


def create_refresh_token(subject: Union[str, Any]) -> str:
    return _create_token(
        subject,
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
        expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        token_type=TokenType.REFRESH,
    )


def decode_token(token: str, token_type: TokenType) -> dict[str, Any]:
    """Verify signature + expiry and return the claims.

    Picks the correct secret based on the expected token type and asserts
    the `type` claim matches — so a refresh token can never be used as an
    access token. Raises jwt.InvalidTokenError (or a subclass) on failure;
    the caller (dependencies.py) turns that into a 401.
    """
    secret_key = (
        settings.JWT_SECRET_KEY
        if token_type == TokenType.ACCESS
        else settings.JWT_REFRESH_SECRET_KEY
    )
    payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
    if payload.get("type") != token_type.value:
        raise jwt.InvalidTokenError(
            f"Expected a '{token_type.value}' token, got '{payload.get('type')}'"
        )
    return payload
