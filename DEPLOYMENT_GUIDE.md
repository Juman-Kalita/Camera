# 🚀 Full Deployment Guide

## Overview
This guide will help you deploy your Workplace Activity Analytics System to the cloud.

**Stack:**
- Database: Supabase (PostgreSQL)
- Backend: Railway or Render
- Frontend: Vercel or Netlify

---

## Step 1: Setup Supabase Database ✅

1. Go to your Supabase project dashboard
2. Click **SQL Editor** in the left sidebar
3. Copy and paste the contents of `supabase_setup.sql`
4. Click **Run** to create tables
5. Go to **Settings** → **Database**
6. Copy your **Connection String** (URI format)

---

## Step 2: Deploy Backend (Choose One)

### Option A: Railway (Recommended - Easiest)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your `workplace-ai` repository
5. Add environment variables:
   ```
   DATABASE_URL=your_supabase_connection_string
   CAMERA_SOURCE=http
   CAMERA_HTTP_URL=http://10.38.254.194:8080/video
   ```
6. Railway will auto-deploy!
7. Copy your backend URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New** → **Web Service**
4. Connect your GitHub repository
5. Configure:
   - **Build Command:** `pip install -r requirements-deploy.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Click **Create Web Service**
8. Copy your backend URL

---

## Step 3: Update Frontend

1. Open `frontend/dashboard.html`
2. Find line: `const API_URL = 'http://localhost:8000';`
3. Replace with your backend URL: `const API_URL = 'https://your-backend-url.com';`

---

## Step 4: Deploy Frontend (Choose One)

### Option A: Vercel (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click **Add New** → **Project**
4. Import your `workplace-ai` repository
5. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** (leave empty)
   - **Output Directory:** `.`
6. Click **Deploy**
7. Your dashboard will be live at `https://your-app.vercel.app`

### Option B: Netlify

1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click **Add new site** → **Import an existing project**
4. Select your repository
5. Configure:
   - **Base directory:** `frontend`
   - **Build command:** (leave empty)
   - **Publish directory:** `.`
6. Click **Deploy**

---

## Step 5: Update Backend CORS

1. Go back to your backend code
2. Update `main.py` CORS settings with your frontend URL:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```
3. Commit and push changes
4. Backend will auto-redeploy

---

## Step 6: Test Everything

1. Open your frontend URL
2. Check if:
   - ✅ Live video feed loads
   - ✅ Stats update every 2 seconds
   - ✅ Activity logs appear
   - ✅ Charts display data

---

## Important Notes

### Camera Access
- Your phone camera must be accessible from the internet
- Options:
  1. **Port forwarding** on your router (forward port 8080)
  2. **Ngrok tunnel:** `ngrok http 8080` (easier for testing)
  3. **Tailscale/ZeroTier** (secure VPN)

### Costs
- Supabase: FREE (500 MB database)
- Railway: FREE tier ($5 credit/month, ~500 hours)
- Render: FREE tier (spins down after 15 min inactivity)
- Vercel: FREE (unlimited bandwidth for personal)

### Security
- Add authentication later if needed
- Use environment variables for secrets
- Enable HTTPS (automatic on all platforms)

---

## Troubleshooting

**Backend won't start:**
- Check environment variables are set
- Verify DATABASE_URL is correct
- Check logs in Railway/Render dashboard

**Frontend can't connect:**
- Update CORS settings in backend
- Verify API_URL in dashboard.html
- Check browser console for errors

**Camera not connecting:**
- Ensure phone IP hasn't changed
- Check if port 8080 is accessible
- Try ngrok for testing

---

## Next Steps

1. Set up custom domain (optional)
2. Add authentication
3. Enable email alerts
4. Add data export features
5. Create mobile app

Need help? Let me know!
