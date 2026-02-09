import os
from typing import Any, Dict, List, Optional, Union

from pydantic import ConfigDict, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

env_path = os.path.join(os.getcwd(), ".env")


class Settings(BaseSettings):
    model_config = ConfigDict(from_attributes=True)

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    PROJECT_VERSION: str

    ENVIRONMENT: str
    ALGORITHM: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

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

    @field_validator("DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=f"{values.get('POSTGRES_PASSWORD')}",
            host=f"{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
