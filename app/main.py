from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
async def startup():
    logging.info("Starting up...")
    try:
        init_db()
    except Exception as e:
        logging.warning(f"DB init failed: {e}")


@app.on_event("shutdown")
async def shutdown():
    logging.info("Shutting down...")


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": settings.DOCS_URL,
    }
