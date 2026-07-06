from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Response body returned by /login and /refresh.

    `token_type` is "bearer" by convention — it tells the client to send
    the token as `Authorization: Bearer <access_token>`.
    """

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """The decoded contents (claims) of a JWT.

    - sub: the subject == the user id (string).
    - exp: expiry (epoch seconds). PyJWT validates it automatically.
    - type: "access" or "refresh" — so a refresh token can never be
      accepted where an access token is required, and vice versa.
    """

    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None
