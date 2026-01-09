from fastapi import APIRouter
from app.routes import zones

router = APIRouter()

# Include routers
router.include_router(zones.router)

__all__ = ["router"]
