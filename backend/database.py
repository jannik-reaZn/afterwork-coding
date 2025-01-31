from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

SQLITE_DATABASE_URL = "sqlite:///backend/development.db"

engine = create_engine(SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
