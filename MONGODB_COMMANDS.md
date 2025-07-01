# MongoDB Exploration Commands for CrowdGuard DBMS

This document provides comprehensive mongosh commands to explore and query your CrowdGuard database instance.

## Database Information
- **Database Name**: `crowdguard_db`
- **Connection String**: `mongodb://localhost:27017`
- **Collections**: `users`, `zones`, `crowd_data`, `alerts`, `logs`

## 1. Connect to MongoDB
```bash
mongosh
```

## 2. Switch to your database
```javascript
use crowdguard_db
```

## 3. View all collections in your database
```javascript
show collections
```

## 4. Explore Users Collection
```javascript
// View all users
db.users.find().pretty()

// Count total users
db.users.countDocuments()

// Find users by role
db.users.find({role: "Security Officer"}).pretty()

// Find user by ID
db.users.findOne({user_id: "admin"})
```

## 5. Explore Zones Collection
```javascript
// View all zones
db.zones.find().pretty()

// Count total zones
db.zones.countDocuments()

// Find zones by capacity range
db.zones.find({capacity: {$gte: 300}}).pretty()

// Find zone by ID
db.zones.findOne({zone_id: "Z01"})
```

## 6. Explore Crowd Data Collection
```javascript
// View all crowd data (limit to 10 for readability)
db.crowd_data.find().limit(10).pretty()

// Count total crowd data entries
db.crowd_data.countDocuments()

// Find crowd data by density level
db.crowd_data.find({density_level: "High"}).pretty()

// Find crowd data for specific zone
db.crowd_data.find({zone_id: "Z01"}).sort({timestamp: -1}).limit(5).pretty()

// Find recent crowd data (last 10 entries)
db.crowd_data.find().sort({timestamp: -1}).limit(10).pretty()
```

## 7. Explore Alerts Collection
```javascript
// View all alerts
db.alerts.find().pretty()

// Count total alerts
db.alerts.countDocuments()

// Find active alerts
db.alerts.find({status: "Active"}).pretty()

// Find alerts by severity
db.alerts.find({severity: "High"}).pretty()

// Find alerts for specific zone
db.alerts.find({zone_id: "Z03"}).pretty()
```

## 8. Explore Logs Collection
```javascript
// View all logs
db.logs.find().pretty()

// Count total logs
db.logs.countDocuments()

// Find recent logs (last 5)
db.logs.find().sort({timestamp: -1}).limit(5).pretty()

// Find logs by user
db.logs.find({performed_by: "Security Officer"}).pretty()
```

## 9. Useful Aggregation Queries
```javascript
// Get crowd density statistics by zone
db.crowd_data.aggregate([
  {
    $group: {
      _id: "$zone_id",
      avgPeople: {$avg: "$people_count"},
      maxPeople: {$max: "$people_count"},
      minPeople: {$min: "$people_count"},
      totalReadings: {$sum: 1}
    }
  }
]).pretty()

// Get alert statistics by severity
db.alerts.aggregate([
  {
    $group: {
      _id: "$severity",
      count: {$sum: 1}
    }
  }
]).pretty()

// Get users by role
db.users.aggregate([
  {
    $group: {
      _id: "$role",
      count: {$sum: 1},
      users: {$push: "$name"}
    }
  }
]).pretty()
```

## 10. Database Statistics
```javascript
// Get database stats
db.stats()

// Get collection stats
db.users.stats()
db.zones.stats()
db.crowd_data.stats()
db.alerts.stats()
db.logs.stats()
```

## Quick Summary Commands
If you want to quickly see what's in your database, run these commands in sequence:

```javascript
use crowdguard_db
show collections
print("=== USERS ===")
db.users.find().pretty()
print("=== ZONES ===")
db.zones.find().pretty()
print("=== RECENT CROWD DATA (5 entries) ===")
db.crowd_data.find().sort({timestamp: -1}).limit(5).pretty()
print("=== ACTIVE ALERTS ===")
db.alerts.find({status: "Active"}).pretty()
print("=== RECENT LOGS (5 entries) ===")
db.logs.find().sort({timestamp: -1}).limit(5).pretty()
```

## Expected Data (Based on Seed Data)

Based on your seed data, you should see:

### Users (3 total)
- **admin** - Admin User (Admin role)
- **officer1** - Security Officer (Security Officer role, assigned to Z01)
- **organizer** - Event Organizer (Event Organizer role)

### Zones (6 total)
- **Z01** - Main Gate (capacity: 300)
- **Z02** - Food Court (capacity: 200)
- **Z03** - Stage Area (capacity: 500)
- **Z04** - Parking Lot (capacity: 150)
- **Z05** - Exit Gate (capacity: 250)
- **Z06** - Prayer Hall (capacity: 400)

### Sample Data
- Multiple crowd data entries with random people counts
- 3 alerts (1 active, 1 acknowledged, 1 resolved)
- 3 system logs

## Advanced Queries

### Find High Density Zones
```javascript
db.crowd_data.find({density_level: "High"}).sort({timestamp: -1}).limit(10).pretty()
```

### Find Overcrowded Zones (people count > capacity)
```javascript
db.crowd_data.aggregate([
  {
    $lookup: {
      from: "zones",
      localField: "zone_id",
      foreignField: "zone_id",
      as: "zone_info"
    }
  },
  {
    $unwind: "$zone_info"
  },
  {
    $match: {
      $expr: {
        $gt: ["$people_count", "$zone_info.capacity"]
      }
    }
  }
]).pretty()
```

### Get Zone Performance Summary
```javascript
db.crowd_data.aggregate([
  {
    $lookup: {
      from: "zones",
      localField: "zone_id",
      foreignField: "zone_id",
      as: "zone_info"
    }
  },
  {
    $unwind: "$zone_info"
  },
  {
    $group: {
      _id: "$zone_id",
      locationName: {$first: "$zone_info.location_name"},
      capacity: {$first: "$zone_info.capacity"},
      avgPeople: {$avg: "$people_count"},
      maxPeople: {$max: "$people_count"},
      highDensityCount: {
        $sum: {
          $cond: [{$eq: ["$density_level", "High"]}, 1, 0]
        }
      },
      totalReadings: {$sum: 1}
    }
  },
  {
    $addFields: {
      utilizationPercent: {
        $multiply: [
          {$divide: ["$avgPeople", "$capacity"]},
          100
        ]
      }
    }
  }
]).pretty()
```

## Troubleshooting

### If you can't connect to MongoDB:
1. Make sure MongoDB is running: `brew services start mongodb-community` (on macOS)
2. Check if the service is running: `brew services list | grep mongodb`
3. Try connecting with explicit host: `mongosh mongodb://localhost:27017`

### If the database doesn't exist:
1. Run the seed script: `python backend/seed_data.py`
2. Or start the application to create the database structure

### If collections are empty:
1. Check if seed data was run
2. Run the mock data generator: `python backend/mock_data.py`
3. Or use the start script: `./start_with_mock.sh`


