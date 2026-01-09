from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/delivery_management"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
