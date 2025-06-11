from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    user_id: str
    name: str
    role: str
    contact: str
    zone_assigned: Optional[str] = None
    password: str

class Zone(BaseModel):
    zone_id: str
    location_name: str
    capacity: int

class CrowdData(BaseModel):
    zone_id: str
    timestamp: str
    people_count: int
    density_level: str

class Alert(BaseModel):
    alert_id: str
    zone_id: str
    severity: str
    time: str
    status: str
    responder: Optional[str] = None

class Log(BaseModel):
    log_id: str
    action: str
    performed_by: str
    timestamp: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AlertUpdate(BaseModel):
    status: str
    responder: Optional[str] = None



