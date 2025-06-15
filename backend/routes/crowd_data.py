from fastapi import APIRouter
from backend.database import crowd_data_collection
from backend.models import CrowdData
from typing import Optional

router = APIRouter()

@router.get("/crowd-data")
async def get_crowd_data(zone_id: Optional[str] = None):
    query = {}
    if zone_id:
        query["zone_id"] = zone_id
    
    crowd_data = []
    async for data in crowd_data_collection.find(query).sort("timestamp", -1).limit(50):
        data.pop("_id")
        crowd_data.append(data)
    return crowd_data

@router.get("/crowd-data/latest")
async def get_latest_crowd_data():
    # Get the most recent crowd data for each zone
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$zone_id",
            "zone_id": {"$first": "$zone_id"},
            "timestamp": {"$first": "$timestamp"},
            "people_count": {"$first": "$people_count"},
            "density_level": {"$first": "$density_level"}
        }},
        {"$project": {"_id": 0}}
    ]
    
    latest_data = []
    async for data in crowd_data_collection.aggregate(pipeline):
        latest_data.append(data)
    return latest_data

@router.post("/crowd-data")
async def add_crowd_data(data: CrowdData):
    await crowd_data_collection.insert_one(data.dict())
    return {"message": "Crowd data added successfully"}



