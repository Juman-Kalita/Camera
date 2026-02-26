# 🚀 Simple Deployment Guide (No Database)

## Overview
Deploy your Workplace Activity Analytics System without database persistence.
All data is stored in memory (resets on restart).

**Stack:**
- Backend: Railway or Render (Python FastAPI + AI)
- Frontend: Vercel or Netlify (Static HTML)
- Storage: In-memory only (no database needed)

---

## ✅ Quick Deployment Checklist

### Step 1: Deploy Backend to Railway (10 minutes)

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `workplace-ai` repository
   - Railway will auto-detect and deploy

3. **Add Environment Variables**
   - Click on your service → "Variables" tab
   - Add these:
     ```
     CAMERA_SOURCE=http
     CAMERA_HTTP_URL=http://10.38.254.194:8080/video
     ```

4. **Generate Domain**
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Copy your URL (e.g., `https://workplace-ai-production.up.railway.app`)

5. **Test Backend**
   - Open `https://your-url.railway.app/` in browser
   - Should see: `{"message": "Workplace Activity Analytics API", "status": "running"}`

---

### Step 2: Update Frontend (2 minutes)

1. **Edit dashboard.html**
   - Open `frontend/dashboard.html`
   - Find line: `const API_URL = 'http://localhost:8000';`
   - Replace with: `const API_URL = 'https://your-railway-url.railway.app';`
   - Save file

2. **Commit Changes**
   ```bash
   git add .
   git commit -m "Update API URL for deployment"
   git push
   ```

---

### Step 3: Deploy Frontend to Vercel (5 minutes)

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Select your `workplace-ai` repository

3. **Configure Deployment**
   - **Root Directory:** `frontend`
   - **Framework Preset:** Other
   - **Build Command:** (leave empty)
   - **Output Directory:** `.`

4. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Copy your URL (e.g., `https://workplace-ai.vercel.app`)

---

### Step 4: Fix CORS (3 minutes)

1. **Update Backend CORS**
   - Open `backend/main.py`
   - Find: `allow_origins=["*"]`
   - Replace with: `allow_origins=["https://your-vercel-url.vercel.app"]`

2. **Commit and Push**
   ```bash
   git add .
   git commit -m "Update CORS for production"
   git push
   ```

3. **Railway Auto-Redeploys**
   - Wait 1-2 minutes for Railway to redeploy

---

### Step 5: Setup Camera Access (Choose One)

#### Option A: Ngrok (Easiest - For Testing)

1. **Download Ngrok**
   - Go to https://ngrok.com/download
   - Install for your OS

2. **Start Tunnel**
   ```bash
   ngrok http 8080
   ```

3. **Copy HTTPS URL**
   - Look for: `Forwarding https://abc123.ngrok.io -> http://localhost:8080`
   - Copy the HTTPS URL

4. **Update Railway**
   - Go to Railway → Variables
   - Update: `CAMERA_HTTP_URL=https://abc123.ngrok.io/video`
   - Service will auto-restart

#### Option B: Port Forwarding (Permanent)

1. **Access Router**
   - Open router admin (usually 192.168.1.1)
   - Login with admin credentials

2. **Setup Port Forward**
   - Find "Port Forwarding" or "Virtual Server"
   - Add rule:
     - External Port: 8080
     - Internal IP: 10.38.254.194
     - Internal Port: 8080
     - Protocol: TCP

3. **Get Public IP**
   - Visit https://whatismyipaddress.com
   - Copy your public IP

4. **Update Railway**
   - Go to Railway → Variables
   - Update: `CAMERA_HTTP_URL=http://YOUR_PUBLIC_IP:8080/video`

---

### Step 6: Test Everything ✅

1. **Open Your Dashboard**
   - Go to your Vercel URL
   - Should see the dashboard load

2. **Check Video Feed**
   - Live camera feed should appear
   - May take 5-10 seconds to load

3. **Verify Stats**
   - Stats should update every 2 seconds
   - Activity logs should appear in table

4. **Test for 5 Minutes**
   - Move around, use phone
   - Check if detection works

---

## 📊 What You Get

**Features:**
- ✅ Real-time person detection
- ✅ Posture tracking (sitting/standing)
- ✅ Phone usage detection
- ✅ Activity classification
- ✅ Live stats and charts
- ✅ Recent activity logs (last 1000 entries)

**Limitations:**
- ⚠️ Data resets when backend restarts
- ⚠️ No historical data storage
- ⚠️ Logs limited to last 1000 entries

---

## 💰 Costs

**Total: $0/month**

- Railway: FREE ($5 credit/month, ~500 hours)
- Vercel: FREE (unlimited for personal projects)
- Ngrok: FREE (1 tunnel, resets on restart)

---

## 🔧 Troubleshooting

**Backend won't start:**
- Check Railway logs for errors
- Verify environment variables are set
- Make sure requirements-deploy.txt is correct

**Frontend can't connect:**
- Check CORS settings in main.py
- Verify API_URL in dashboard.html
- Open browser console (F12) for errors

**Camera not connecting:**
- Ensure phone IP Webcam app is running
- Check if ngrok tunnel is active
- Verify CAMERA_HTTP_URL is correct

**Video is laggy:**
- Check your internet upload speed
- Try reducing video quality in IP Webcam app
- Consider using RTSP instead of HTTP

---

## 🎯 Next Steps

**Want to add database later?**
- Follow the full deployment guide
- Add Supabase (free PostgreSQL)
- Switch to database_postgres.py

**Want better performance?**
- Upgrade Railway plan ($5/month)
- Use dedicated server
- Add Redis for caching

**Want more features?**
- Add authentication
- Enable email alerts
- Create mobile app
- Add multi-camera support

---

## 📞 Need Help?

If you get stuck:
1. Check Railway logs: Railway Dashboard → Your Service → Logs
2. Check browser console: F12 → Console tab
3. Verify all URLs are correct
4. Make sure phone camera is accessible

Ready to deploy? Start with Step 1!
