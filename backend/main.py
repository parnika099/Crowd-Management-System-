from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes import users, zones, crowd_data, alerts
from backend.database import logs_collection
import os

app = FastAPI(title="CrowdGuard API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, tags=["Users"])
app.include_router(zones.router, tags=["Zones"])
app.include_router(crowd_data.router, tags=["Crowd Data"])
app.include_router(alerts.router, tags=["Alerts"])

# Serve static files (frontend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/logs")
async def get_logs(limit: int = 20):
    logs = []
    async for log in logs_collection.find().sort("timestamp", -1).limit(limit):
        log.pop("_id")
        logs.append(log)
    return logs

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



