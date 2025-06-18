import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import random
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "crowdguard_db"

async def generate_mock_data():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    
    zones_collection = db["zones"]
    crowd_data_collection = db["crowd_data"]
    alerts_collection = db["alerts"]
    
    print("Mock data generator started...")
    
    while True:
        # Get all zones
        zones = await zones_collection.find().to_list(length=100)
        
        for zone in zones:
            # Generate random crowd count
            people_count = random.randint(30, int(zone["capacity"] * 1.1))
            
            # Determine density level
            capacity = zone["capacity"]
            if people_count > capacity * 0.8:
                density_level = "High"
            elif people_count > capacity * 0.5:
                density_level = "Medium"
            else:
                density_level = "Low"
            
            # Insert crowd data
            crowd_entry = {
                "zone_id": zone["zone_id"],
                "timestamp": datetime.now().isoformat(),
                "people_count": people_count,
                "density_level": density_level
            }
            await crowd_data_collection.insert_one(crowd_entry)
            
            # Create alert if high density
            if density_level == "High":
                # Check if there's already an active alert for this zone
                existing_alert = await alerts_collection.find_one({
                    "zone_id": zone["zone_id"],
                    "status": "Active"
                })
                
                if not existing_alert:
                    alert_id = f"A{datetime.now().strftime('%Y%m%d%H%M%S')}{zone['zone_id']}"
                    severity = "High" if people_count > capacity else "Medium"
                    
                    alert_entry = {
                        "alert_id": alert_id,
                        "zone_id": zone["zone_id"],
                        "severity": severity,
                        "time": datetime.now().isoformat(),
                        "status": "Active",
                        "responder": None
                    }
                    await alerts_collection.insert_one(alert_entry)
                    print(f"Alert created for zone {zone['zone_id']}: {severity} density")
        
        print(f"Generated data at {datetime.now().strftime('%H:%M:%S')}")
        await asyncio.sleep(10)  # Generate data every 10 seconds

if __name__ == "__main__":
    asyncio.run(generate_mock_data())



