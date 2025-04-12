from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from backend.common.config import Settings, get_settings
from backend.database import get_db
from backend.main import app

SQLITE_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Recreate the database schema before each test."""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a new database session with a rollback at the end of the test."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_settings() -> Settings:
    """Override the settings for tests."""
    return Settings(
        app_name="Test App",
        cors_origins=["http://localhost:3000"],
        # secret_key_jwt="test_secret",
        # algorithm_jwt="HS256",
        verbose_database_logging=True,
    )


@pytest.fixture(scope="function", autouse=True)
def override_settings(test_settings: Settings):
    """Override FastAPI settings dependency for all tests."""
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield
    app.dependency_overrides.pop(get_settings, None)


@pytest.fixture(scope="function")
def test_client(db_session: Generator[Session, None, None]):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
