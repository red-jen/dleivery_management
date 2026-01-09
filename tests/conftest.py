"""
Test fixtures and configuration for the test suite.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database.connection import Base, get_db
from app.models import Zone


# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with overridden database dependency."""
    app.dependency_overrides[get_db] = lambda: db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_zone(db):
    """Create a sample zone for testing."""
    zone = Zone(nom="Paris", code_postal="75001")
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone
