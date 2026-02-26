# ✅ Deployment Checklist

Follow these steps in order:

## 1. Supabase Setup (5 minutes)
- [ ] Copy `supabase_setup.sql` content
- [ ] Go to Supabase → SQL Editor
- [ ] Paste and run the SQL
- [ ] Verify tables created (should see `activity_logs` and `time_summary`)
- [ ] Go to Settings → Database
- [ ] Copy your connection string (starts with `postgresql://`)
- [ ] Save it somewhere safe

## 2. Prepare Code for Deployment (2 minutes)
- [ ] Open `backend/main.py`
- [ ] Replace `from database import Database` with `from database_postgres import Database`
- [ ] Update database initialization to use environment variable
- [ ] Commit changes to GitHub

## 3. Deploy Backend - Railway (10 minutes)
- [ ] Go to https://railway.app
- [ ] Sign up with GitHub
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select `workplace-ai` repository
- [ ] Click on the service → Variables
- [ ] Add these environment variables:
  ```
  DATABASE_URL = your_supabase_connection_string
  CAMERA_SOURCE = http
  CAMERA_HTTP_URL = http://10.38.254.194:8080/video
  ```
- [ ] Wait for deployment to complete
- [ ] Click "Settings" → "Networking" → "Generate Domain"
- [ ] Copy your backend URL (e.g., `https://workplace-ai-production.up.railway.app`)
- [ ] Test: Open `https://your-url.railway.app/` in browser (should see API message)

## 4. Update Frontend (2 minutes)
- [ ] Open `frontend/dashboard.html`
- [ ] Find: `const API_URL = 'http://localhost:8000';`
- [ ] Replace with: `const API_URL = 'https://your-railway-url.railway.app';`
- [ ] Save and commit to GitHub

## 5. Deploy Frontend - Vercel (5 minutes)
- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "Add New" → "Project"
- [ ] Import `workplace-ai` repository
- [ ] Configure:
  - Root Directory: `frontend`
  - Framework Preset: Other
  - Build Command: (leave empty)
  - Output Directory: `.`
- [ ] Click "Deploy"
- [ ] Wait for deployment
- [ ] Copy your frontend URL (e.g., `https://workplace-ai.vercel.app`)
- [ ] Open it in browser

## 6. Fix CORS (3 minutes)
- [ ] Go back to your code
- [ ] Open `backend/main.py`
- [ ] Find `allow_origins=["*"]`
- [ ] Replace with: `allow_origins=["https://your-vercel-url.vercel.app"]`
- [ ] Commit and push to GitHub
- [ ] Railway will auto-redeploy

## 7. Setup Camera Access (10 minutes)

### Option A: Ngrok (Easiest for testing)
- [ ] Download ngrok: https://ngrok.com/download
- [ ] Run: `ngrok http 8080`
- [ ] Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
- [ ] Update Railway environment variable:
  ```
  CAMERA_HTTP_URL = https://abc123.ngrok.io/video
  ```

### Option B: Port Forwarding (Permanent)
- [ ] Log into your router admin panel
- [ ] Find "Port Forwarding" settings
- [ ] Forward external port 8080 to your phone's IP (10.38.254.194:8080)
- [ ] Get your public IP: https://whatismyipaddress.com
- [ ] Update Railway environment variable:
  ```
  CAMERA_HTTP_URL = http://YOUR_PUBLIC_IP:8080/video
  ```

## 8. Final Testing
- [ ] Open your Vercel frontend URL
- [ ] Check video feed loads
- [ ] Verify stats are updating
- [ ] Check activity logs appear
- [ ] Test for 5 minutes to ensure stability

## 9. Optional Enhancements
- [ ] Add custom domain to Vercel
- [ ] Set up authentication
- [ ] Enable email notifications
- [ ] Add data export feature

---

## Quick Reference

**Your URLs:**
- Supabase Dashboard: https://supabase.com/dashboard
- Railway Backend: https://railway.app/dashboard
- Vercel Frontend: https://vercel.com/dashboard
- Ngrok Dashboard: https://dashboard.ngrok.com

**Estimated Total Time:** 30-40 minutes

**Total Cost:** $0/month (all free tiers)

---

## Need Help?

If you get stuck:
1. Check the logs in Railway dashboard
2. Open browser console (F12) to see errors
3. Verify all environment variables are set correctly
4. Make sure phone camera app is running

Let me know if you need assistance!
