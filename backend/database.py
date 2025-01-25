from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///backend/development.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
