from fastapi import APIRouter, HTTPException
from backend.database import users_collection, logs_collection
from backend.models import LoginRequest, User
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest):
    user = await users_collection.find_one({
        "user_id": request.username,
        "password": request.password
    })
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Log the login action
    log_entry = {
        "log_id": f"LOG{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "action": f"User {user['name']} logged in",
        "performed_by": user["name"],
        "timestamp": datetime.now().isoformat()
    }
    await logs_collection.insert_one(log_entry)
    
    return {
        "message": "Login successful",
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "role": user["role"],
            "zone_assigned": user.get("zone_assigned")
        }
    }

@router.get("/users")
async def get_users():
    users = []
    async for user in users_collection.find():
        user.pop("_id")
        user.pop("password")
        users.append(user)
    return users

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await users_collection.find_one({"user_id": user_id})
    if user:
        user.pop("_id")
        user.pop("password")
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users")
async def create_user(user: User):
    # Check if user already exists
    existing_user = await users_collection.find_one({"user_id": user.user_id})
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already exists")
    
    await users_collection.insert_one(user.dict())
    return {"message": "User created successfully"}

@router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: dict):
    # Check if user exists
    existing_user = await users_collection.find_one({"user_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user
    result = await users_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")
    
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    # Check if user exists
    existing_user = await users_collection.find_one({"user_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    result = await users_collection.delete_one({"user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="User could not be deleted")
    
    return {"message": "User deleted successfully"}


