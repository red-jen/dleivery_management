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
    existing = db.query(Zone).filter(Zone.code_postal == zone.code_postal).first()
    if existing:
        raise HTTPException(status_code=400, detail="Zone with this postal code already exists")
    
    db_zone = Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone


@router.get("/", response_model=List[ZoneSchema])
async def list_zones(db: Session = Depends(get_db)):
    return db.query(Zone).all()


@router.get("/{zone_id}", response_model=ZoneSchema)
async def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone


@router.put("/{zone_id}", response_model=ZoneSchema)
async def update_zone(zone_id: int, zone_update: ZoneUpdate, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    for field, value in zone_update.dict(exclude_unset=True).items():
        setattr(zone, field, value)
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    db.delete(zone)
    db.commit()
        raise HTTPException(status_code=500, detail="Error deleting zone")
