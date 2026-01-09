from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings, logger
from app.database import init_db

# Create FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

# Configure CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions globally."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "type": type(exc).__name__,
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
        logger.info("Continuing without database. Check your DATABASE_URL in .env")
    logger.info(f"Application '{settings.APP_NAME}' started")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info(f"Application '{settings.APP_NAME}' shutting down")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.APP_NAME}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": settings.DOCS_URL,
    }
