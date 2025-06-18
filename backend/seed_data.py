from backend.database import get_sync_database
from datetime import datetime, timedelta
import random

def seed_database():
    db = get_sync_database()
    
    # Clear existing data
    print("Clearing existing data...")
    db.users.delete_many({})
    db.zones.delete_many({})
    db.crowd_data.delete_many({})
    db.alerts.delete_many({})
    db.logs.delete_many({})
    
    # Seed Users
    print("Seeding users...")
    users = [
        {
            "user_id": "admin",
            "name": "Admin User",
            "role": "Admin",
            "contact": "+91-9876543210",
            "zone_assigned": None,
            "password": "admin123"
        },
        {
            "user_id": "officer1",
            "name": "Security Officer",
            "role": "Security Officer",
            "contact": "+91-9876543211",
            "zone_assigned": "Z01",
            "password": "officer123"
        },
        {
            "user_id": "organizer",
            "name": "Event Organizer",
            "role": "Event Organizer",
            "contact": "+91-9876543212",
            "zone_assigned": None,
            "password": "org123"
        }
    ]
    db.users.insert_many(users)
    
    # Seed Zones
    print("Seeding zones...")
    zones = [
        {"zone_id": "Z01", "location_name": "Main Gate", "capacity": 300},
        {"zone_id": "Z02", "location_name": "Food Court", "capacity": 200},
        {"zone_id": "Z03", "location_name": "Stage Area", "capacity": 500},
        {"zone_id": "Z04", "location_name": "Parking Lot", "capacity": 150},
        {"zone_id": "Z05", "location_name": "Exit Gate", "capacity": 250},
        {"zone_id": "Z06", "location_name": "Prayer Hall", "capacity": 400}
    ]
    db.zones.insert_many(zones)
    
    # Seed initial crowd data
    print("Seeding crowd data...")
    crowd_data = []
    for zone in zones:
        for i in range(5):
            time_offset = timedelta(minutes=i * 10)
            people_count = random.randint(50, int(zone["capacity"] * 0.7))
            density_level = "Low"
            if people_count > zone["capacity"] * 0.8:
                density_level = "High"
            elif people_count > zone["capacity"] * 0.5:
                density_level = "Medium"
            
            crowd_data.append({
                "zone_id": zone["zone_id"],
                "timestamp": (datetime.now() - time_offset).isoformat(),
                "people_count": people_count,
                "density_level": density_level
            })
    db.crowd_data.insert_many(crowd_data)
    
    # Seed some alerts
    print("Seeding alerts...")
    alerts = [
        {
            "alert_id": "A001",
            "zone_id": "Z03",
            "severity": "High",
            "time": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "status": "Active",
            "responder": None
        },
        {
            "alert_id": "A002",
            "zone_id": "Z01",
            "severity": "Medium",
            "time": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "status": "Acknowledged",
            "responder": "Security Officer"
        },
        {
            "alert_id": "A003",
            "zone_id": "Z02",
            "severity": "Low",
            "time": (datetime.now() - timedelta(hours=1)).isoformat(),
            "status": "Resolved",
            "responder": "Security Officer"
        }
    ]
    db.alerts.insert_many(alerts)
    
    # Seed logs
    print("Seeding logs...")
    logs = [
        {
            "log_id": "LOG001",
            "action": "System initialized",
            "performed_by": "System",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            "log_id": "LOG002",
            "action": "Alert A001 created for zone Z03",
            "performed_by": "System",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat()
        },
        {
            "log_id": "LOG003",
            "action": "Alert A002 acknowledged by Security Officer",
            "performed_by": "Security Officer",
            "timestamp": (datetime.now() - timedelta(minutes=25)).isoformat()
        }
    ]
    db.logs.insert_many(logs)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()



