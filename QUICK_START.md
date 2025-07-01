# 🚀 Quick Start Guide

## Fastest Way to Run CrowdGuard

This project uses **uv** for virtual environment and dependency management.

### Step 1: Install uv (if needed)
```bash
# macOS
brew install uv

# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Start MongoDB
**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongodb
```

**Or use MongoDB Atlas** (Cloud - Free):
1. Go to https://mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Export: `export MONGO_URL="your_connection_string"`

### Step 3: Run the Application

**Option A: Simple Start (Recommended)**
```bash
./start.sh
```

**Option B: With Real-time Mock Data**
```bash
./start_with_mock.sh
```

**Option C: Manual Steps**
```bash
uv sync                    # create .venv and install deps (first time)
uv run python -m backend.seed_data   # seed database (first time only)
uv run uvicorn backend.main:app --reload   # start server

# Optional: In another terminal, start mock data generator
uv run python -m backend.mock_data
```

### Step 4: Open Dashboard
Open browser: http://localhost:8000/index.html

### Login Credentials
- **Admin**: `admin` / `admin123`
- **Officer**: `officer1` / `officer123`
- **Organizer**: `organizer` / `org123`

---

## What You'll See

1. **Login Page**: Enter credentials
2. **Dashboard**: 
   - Zone status cards (color-coded by density)
   - Active alerts section
   - Activity logs table
3. **Real-time Updates**: Auto-refresh every 5 seconds

---

## Troubleshooting

**Error: Connection refused**
→ MongoDB not running. Start it first.

**Error: Module not found**
→ Run: `uv sync`

**Port 8000 already in use**
→ Kill existing process: `lsof -ti:8000 | xargs kill -9`

---

## API Documentation
Interactive API docs: http://localhost:8000/docs

---

## Project Features

✅ Real-time crowd monitoring  
✅ Automatic alert generation  
✅ Role-based access (Admin/Officer/Organizer)  
✅ Color-coded density levels  
✅ Activity logging  
✅ Mock data simulation  
✅ MongoDB aggregation pipelines  
✅ RESTful API with FastAPI  

---

**For detailed documentation, see README.md**



