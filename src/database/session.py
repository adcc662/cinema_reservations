from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.config import settings

database_uri = settings.DATABASE_URI
engine = create_engine(str(database_uri))
metadata = SQLModel.metadata


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
