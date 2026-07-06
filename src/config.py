import os
from functools import lru_cache
from typing import Any, Optional, Union

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.join(os.getcwd(), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    PROJECT_VERSION: str

    ENVIRONMENT: str
    ALGORITHM: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    # Token lifetimes. Defaults are sane, override in .env if needed.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # short-lived
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    SERVER_HOST: str
    SERVER_NAME: str
    FRONTEND_VALIDATION_URL: str

    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URI: Union[PostgresDsn, str, None] = None

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        data = info.data
        user = data.get("POSTGRES_USER", "")
        password = data.get("POSTGRES_PASSWORD", "")
        server = data.get("POSTGRES_SERVER", "")
        port = data.get("POSTGRES_PORT", "5432")
        db = data.get("POSTGRES_DB", "")
        return f"postgresql://{user}:{password}@{server}:{port}/{db}"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    The lru_cache means the .env file and environment are parsed ONCE per
    process. Every caller (FastAPI dependencies, database session, etc.)
    shares the same object instead of re-reading config on each request.
    """
    return Settings()


# Kept for backwards compatibility with modules that import `settings`
# directly (e.g. src/database/session.py). New code should depend on
# get_settings() so it can be overridden in tests.
settings = get_settings()
