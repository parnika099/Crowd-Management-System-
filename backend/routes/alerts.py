from fastapi import APIRouter, HTTPException
from backend.database import alerts_collection, logs_collection
from backend.models import Alert, AlertUpdate
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/alerts")
async def get_alerts(status: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status
    
    alerts = []
    async for alert in alerts_collection.find(query).sort("time", -1).limit(20):
        alert.pop("_id")
        alerts.append(alert)
    return alerts

@router.put("/alerts/{alert_id}")
async def update_alert(alert_id: str, update: AlertUpdate):
    result = await alerts_collection.update_one(
        {"alert_id": alert_id},
        {"$set": update.dict(exclude_none=True)}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Log the action
    log_entry = {
        "log_id": f"LOG{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "action": f"Alert {alert_id} status updated to {update.status}",
        "performed_by": update.responder or "System",
        "timestamp": datetime.now().isoformat()
    }
    await logs_collection.insert_one(log_entry)
    
    return {"message": "Alert updated successfully"}

@router.post("/alerts")
async def create_alert(alert: Alert):
    await alerts_collection.insert_one(alert.dict())
    
    # Log the action
    log_entry = {
        "log_id": f"LOG{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "action": f"New alert created for zone {alert.zone_id}",
        "performed_by": "System",
        "timestamp": datetime.now().isoformat()
    }
    await logs_collection.insert_one(log_entry)
    
    return {"message": "Alert created successfully"}



