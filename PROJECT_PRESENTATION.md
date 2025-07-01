# 🎓 CrowdGuard - Project Presentation Guide

## For B.Tech DBMS Submission

---

## 1. Project Introduction (2 minutes)

### What is CrowdGuard?
"CrowdGuard is an intelligent crowd management system designed for large public events like Kumbh Mela, concerts, and festivals. It uses MongoDB to store and manage real-time crowd data, automatically generates alerts when zones reach critical density, and provides a dashboard for event organizers and security personnel."

### Problem Statement
- Large gatherings face overcrowding risks
- Need real-time monitoring across multiple zones
- Quick alert system for security personnel
- Historical data for planning

### Solution
- Real-time crowd monitoring dashboard
- Automatic alert generation based on capacity thresholds
- Role-based access for different stakeholders
- MongoDB for flexible, scalable data storage

---

## 2. Technology Stack (1 minute)

| Component | Technology | Why? |
|-----------|------------|------|
| Backend | Python FastAPI | Fast, modern, async API framework |
| Database | MongoDB | Document-based, flexible schema, real-time updates |
| Frontend | HTML/CSS/JS | Simple, responsive web interface |
| Async Driver | Motor | Non-blocking MongoDB operations |

---

## 3. Database Design (3 minutes)

### MongoDB Collections:

#### 1. **users** - Store user credentials and roles
```javascript
{
  user_id: "admin",
  name: "Admin User",
  role: "Admin",
  contact: "+91-9876543210",
  zone_assigned: null,
  password: "admin123"
}
```

#### 2. **zones** - Define monitored areas
```javascript
{
  zone_id: "Z01",
  location_name: "Main Gate",
  capacity: 300
}
```

#### 3. **crowd_data** - Time-series crowd information
```javascript
{
  zone_id: "Z01",
  timestamp: "2025-10-09T10:45:00Z",
  people_count: 285,
  density_level: "High"
}
```

#### 4. **alerts** - Critical alerts for high density
```javascript
{
  alert_id: "A001",
  zone_id: "Z03",
  severity: "High",
  time: "2025-10-09T10:45:00Z",
  status: "Active",
  responder: null
}
```

#### 5. **logs** - System activity tracking
```javascript
{
  log_id: "LOG001",
  action: "Alert acknowledged",
  performed_by: "Security Officer",
  timestamp: "2025-10-09T10:45:00Z"
}
```

### Why MongoDB?
- **Flexible Schema**: Easy to add new fields
- **Document Model**: Natural representation of real-world entities
- **Scalability**: Handles large volumes of time-series data
- **Aggregation**: Powerful queries for analytics
- **Real-time**: Fast reads and writes for live monitoring

---

## 4. Key Features Demo (5 minutes)

### Feature 1: User Authentication
- Login with role-based credentials
- Different access levels (Admin, Officer, Organizer)

### Feature 2: Real-time Zone Monitoring
- Color-coded density levels:
  - 🟢 Green = Low (< 50% capacity)
  - 🟡 Yellow = Medium (50-80% capacity)
  - 🔴 Red = High (> 80% capacity)
- Shows current count vs capacity
- Auto-refreshes every 5 seconds

### Feature 3: Alert Management
- Automatic alert generation when density > 80%
- Alert workflow: Active → Acknowledged → Resolved
- Severity levels: High, Medium, Low
- Track responders

### Feature 4: Activity Logs
- All actions logged with timestamp
- Track user activities
- System event monitoring

### Feature 5: Mock Data Simulation
- Generates realistic crowd data every 10 seconds
- Simulates crowd flow patterns
- Automatic alert triggering

---

## 5. MongoDB Features Demonstrated (3 minutes)

### 1. CRUD Operations
```python
# Create
await collection.insert_one(document)

# Read
await collection.find_one({"zone_id": "Z01"})

# Update
await collection.update_one({"alert_id": id}, {"$set": {"status": "Resolved"}})

# Delete (in seed script)
db.collection.delete_many({})
```

### 2. Aggregation Pipeline
```python
# Get latest crowd data per zone
pipeline = [
    {"$sort": {"timestamp": -1}},
    {"$group": {
        "_id": "$zone_id",
        "zone_id": {"$first": "$zone_id"},
        "timestamp": {"$first": "$timestamp"},
        "people_count": {"$first": "$people_count"}
    }}
]
```

### 3. Queries with Filters
```python
# Filter alerts by status
alerts = await alerts_collection.find({"status": "Active"}).to_list()

# Sort and limit
crowd_data = await crowd_data_collection.find()
    .sort("timestamp", -1)
    .limit(50)
```

### 4. Time-series Data Storage
- Efficient storage of timestamped records
- Quick queries for recent data
- Historical analysis capability

---

## 6. Live Demo Script (5 minutes)

### Step 1: Start the System
```bash
./start_with_mock.sh
```

### Step 2: Login
- Open http://localhost:8000/index.html
- Login as Admin (admin/admin123)

### Step 3: Show Dashboard
- Point out zone cards with different density levels
- Explain color coding
- Show real-time count updates

### Step 4: Demonstrate Alerts
- Point to active alerts section
- Click "Acknowledge" button
- Show status change
- Click "Resolve" button

### Step 5: Show Activity Logs
- Scroll to logs section
- Explain tracking of all actions
- Show timestamp and user information

### Step 6: Show API Documentation
- Navigate to http://localhost:8000/docs
- Show FastAPI Swagger UI
- Demonstrate an API call (e.g., GET /zones)

### Step 7: Show MongoDB Data
```bash
# Open MongoDB shell
mongosh

# Switch to database
use crowdguard_db

# Show collections
show collections

# Query data
db.zones.find().pretty()
db.alerts.find({status: "Active"}).pretty()
db.crowd_data.find().sort({timestamp: -1}).limit(5).pretty()
```

---

## 7. Real-world Applications (1 minute)

1. **Kumbh Mela**: Monitor different ghats and bathing areas
2. **Concerts/Festivals**: Track entry gates, stages, food courts
3. **Shopping Malls**: Monitor parking, entrances during sales
4. **Sports Stadiums**: Track different sections during matches
5. **Religious Gatherings**: Manage crowd flow in temples/churches

---

## 8. Project Highlights for Evaluation (1 minute)

✅ **Complete CRUD Operations**: All MongoDB operations implemented
✅ **Aggregation Pipelines**: Complex queries demonstrated
✅ **Real-time Updates**: Live data monitoring
✅ **RESTful API**: Well-structured endpoints
✅ **Clean Code**: Simple, readable, well-commented
✅ **Documentation**: Comprehensive README and guides
✅ **Practical Use Case**: Addresses real-world problem
✅ **Scalable Design**: Can handle multiple events/zones

---

## 9. Future Enhancements (1 minute)

- 📱 Mobile app for security officers
- 🤖 AI-based crowd prediction
- 📸 Integration with CCTV cameras
- 🗺️ Interactive zone maps with GeoJSON
- 📊 Advanced analytics and reports
- 🔔 SMS/Email notifications
- 🌐 Multi-event support
- 🔐 Enhanced security features

---

## 10. Conclusion

**Key Takeaways:**
- MongoDB is excellent for real-time applications
- Document model provides flexibility
- Aggregation pipeline enables powerful analytics
- FastAPI + MongoDB = Fast, modern web applications

**Thank you for your attention!**

---

## Quick Reference

### Commands
```bash
# Start system
./start_with_mock.sh

# Seed database
python3 -m backend.seed_data

# Access dashboard
http://localhost:8000/index.html

# API docs
http://localhost:8000/docs
```

### Demo Credentials
- Admin: `admin` / `admin123`
- Officer: `officer1` / `officer123`
- Organizer: `organizer` / `org123`

### MongoDB Commands
```javascript
// Show all zones
db.zones.find().pretty()

// Show active alerts
db.alerts.find({status: "Active"}).pretty()

// Count documents
db.crowd_data.countDocuments()

// Aggregation example
db.crowd_data.aggregate([
  {$match: {density_level: "High"}},
  {$group: {_id: "$zone_id", count: {$sum: 1}}}
])
```



