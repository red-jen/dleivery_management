import uvicorn
from app.main import app
from app.routes import router

# Include API routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
