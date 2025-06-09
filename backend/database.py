from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

# MongoDB connection string
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "crowdguard_db"

# Async client for FastAPI
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Collections
users_collection = database["users"]
zones_collection = database["zones"]
crowd_data_collection = database["crowd_data"]
alerts_collection = database["alerts"]
logs_collection = database["logs"]

# Sync client for seeding data
def get_sync_database():
    sync_client = MongoClient(MONGO_URL)
    return sync_client[DATABASE_NAME]



