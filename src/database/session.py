from sqlmodel import Session, SQLModel, create_engine

from src.config import settings

database_uri = settings.DATABASE_URI
engine = create_engine(str(database_uri))
session = Session(engine)
metadata = SQLModel.metadata
