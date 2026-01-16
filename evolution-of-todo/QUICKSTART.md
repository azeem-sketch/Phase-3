# Quick Start Guide - Evolution of Todo

## ✅ Dependencies Installed!
Backend and frontend dependencies are ready.

## 🚀 3 Steps to Run the App

### STEP 1: Create Backend Environment File

**Create this file:** `backend\.env`

**Copy and paste this content:**
```
DATABASE_URL=postgresql://neondb_owner:npg_your_password@ep-your-endpoint.region.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=change-this-to-a-random-secret-key
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

**⚠️ IMPORTANT:** 
- Get your Neon database URL from: https://console.neon.tech
- Replace the DATABASE_URL with your actual Neon connection string
- Change SECRET_KEY to any random string

### STEP 2: Create Frontend Environment File

**Create this file:** `frontend\.env.local`

**Copy and paste this content:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### STEP 3: Start the Servers

**Open TWO terminal windows:**

**Terminal 1 - Backend:**
```powershell
cd evolution-of-todo\backend
# Use the virtual environment Python with the run_server.py script
venv\Scripts\python run_server.py
```

**Terminal 2 - Frontend:**
```powershell
cd evolution-of-todo\frontend
npm run dev
```


## 🌐 Access the App

Once both servers are running:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📝 First Time Setup

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Create an account with email and password
4. Sign in
5. Start creating todos!

## ❓ Don't have Neon Database?

1. Go to https://neon.tech
2. Sign up for free
3. Create a new project
4. Copy the connection string
5. Paste it in `backend\.env` as DATABASE_URL

---

**Need help?** Make sure both terminal windows show the servers running without errors.
