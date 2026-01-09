from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models import Zone
from app.schemas import ZoneCreate, ZoneUpdate, Zone as ZoneSchema

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/zones", tags=["Zones"])


@router.post("/", response_model=ZoneSchema, status_code=status.HTTP_201_CREATED)
async def create_zone(zone: ZoneCreate, db: Session = Depends(get_db)):
    """Create a new zone."""
    try:
        # Check if zone already exists
        existing = db.query(Zone).filter(Zone.code_postal == zone.code_postal).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Zone with this postal code already exists"
            )
        
        db_zone = Zone(**zone.dict())
        db.add(db_zone)
        db.commit()
        db.refresh(db_zone)
        logger.info(f"Zone created: {db_zone.id}")
        return db_zone
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating zone: {e}")
        raise HTTPException(status_code=500, detail="Error creating zone")


@router.get("/", response_model=List[ZoneSchema])
async def list_zones(db: Session = Depends(get_db)):
    """List all zones."""
    zones = db.query(Zone).all()
    return zones


@router.get("/{zone_id}", response_model=ZoneSchema)
async def get_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get a specific zone by ID."""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zone {zone_id} not found"
        )
    return zone


@router.put("/{zone_id}", response_model=ZoneSchema)
async def update_zone(zone_id: int, zone_update: ZoneUpdate, db: Session = Depends(get_db)):
    """Update a zone."""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zone {zone_id} not found"
        )
    
    try:
        update_data = zone_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(zone, field, value)
        
        db.commit()
        db.refresh(zone)
        logger.info(f"Zone updated: {zone.id}")
        return zone
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating zone: {e}")
        raise HTTPException(status_code=500, detail="Error updating zone")


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    """Delete a zone."""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zone {zone_id} not found"
        )
    
    try:
        db.delete(zone)
        db.commit()
        logger.info(f"Zone deleted: {zone_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting zone: {e}")
        raise HTTPException(status_code=500, detail="Error deleting zone")
