import logging
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "YouExpress API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/youexpress_db"
    DATABASE_ECHO: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # API Documentation
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


def configure_logging(log_level: str = "INFO") -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )


# Global settings instance
settings = Settings()

# Configure logging at startup
configure_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)
