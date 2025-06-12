from fastapi import APIRouter, HTTPException
from backend.database import zones_collection
from backend.models import Zone
from typing import Optional

router = APIRouter()

@router.get("/zones")
async def get_zones():
    zones = []
    async for zone in zones_collection.find():
        zone.pop("_id")
        zones.append(zone)
    return zones

@router.get("/zones/{zone_id}")
async def get_zone(zone_id: str):
    zone = await zones_collection.find_one({"zone_id": zone_id})
    if zone:
        zone.pop("_id")
        return zone
    raise HTTPException(status_code=404, detail="Zone not found")

@router.post("/zones")
async def create_zone(zone: Zone):
    # Check if zone already exists
    existing_zone = await zones_collection.find_one({"zone_id": zone.zone_id})
    if existing_zone:
        raise HTTPException(status_code=400, detail="Zone ID already exists")
    
    await zones_collection.insert_one(zone.dict())
    return {"message": "Zone created successfully"}

@router.put("/zones/{zone_id}")
async def update_zone(zone_id: str, zone_data: dict):
    # Check if zone exists
    existing_zone = await zones_collection.find_one({"zone_id": zone_id})
    if not existing_zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Update zone
    result = await zones_collection.update_one(
        {"zone_id": zone_id},
        {"$set": zone_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")
    
    return {"message": "Zone updated successfully"}

@router.delete("/zones/{zone_id}")
async def delete_zone(zone_id: str):
    # Check if zone exists
    existing_zone = await zones_collection.find_one({"zone_id": zone_id})
    if not existing_zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Delete zone
    result = await zones_collection.delete_one({"zone_id": zone_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="Zone could not be deleted")
    
    return {"message": "Zone deleted successfully"}


