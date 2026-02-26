# 🚂 Railway Deployment Guide

## Quick Deploy (10 minutes)

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose "Camera" repository
4. Railway will start deploying automatically

### Step 3: Configure Environment Variables

1. Click on your service (should say "Camera")
2. Go to "Variables" tab
3. Click "New Variable"
4. Add these variables:

```
CAMERA_SOURCE=http
CAMERA_HTTP_URL=http://YOUR_PHONE_IP:8080/video
```

**Note:** You'll update `CAMERA_HTTP_URL` later with actual phone IP

### Step 4: Generate Domain

1. Go to "Settings" tab
2. Scroll to "Networking"
3. Click "Generate Domain"
4. Copy your URL (e.g., `https://camera-production-xxxx.up.railway.app`)

### Step 5: Update Frontend

1. Go to Vercel dashboard
2. Go to your project → "Settings" → "Environment Variables"
3. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
   ```
4. Or manually update `frontend/index.html`:
   - Find: `const API_URL = 'http://localhost:8000';`
   - Replace with: `const API_URL = 'https://your-railway-url.railway.app';`
   - Commit and push to GitHub

### Step 6: Setup Phone Camera

**For You (Admin):**
1. Install "IP Webcam" app on your phone
2. Open app → "Start Server"
3. Note the IP (e.g., `http://192.168.1.100:8080`)
4. Setup ngrok tunnel:
   ```bash
   ngrok http 8080
   ```
5. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
6. Update Railway variable:
   ```
   CAMERA_HTTP_URL=https://abc123.ngrok.io/video
   ```

**For Your Client:**
1. Install "IP Webcam" app
2. Open app → "Start Server"
3. Send you their ngrok URL
4. You update Railway variable with their URL

---

## 🎯 How It Works

```
[Client's Phone Camera] 
    ↓ (via ngrok)
[Railway Backend] 
    ↓ (processes video)
[Vercel Frontend]
    ↓ (displays dashboard)
[Client's Browser]
```

---

## 💰 Costs

- Railway: FREE ($5 credit/month = ~500 hours)
- Ngrok: FREE (1 tunnel, resets on restart)
- Vercel: FREE (unlimited)

**Total: $0/month**

---

## 🔄 Switching Between Users

To monitor different people:

1. Have each person install IP Webcam
2. Each person starts their camera
3. Update Railway `CAMERA_HTTP_URL` variable
4. Railway auto-restarts with new camera

**OR** deploy multiple Railway instances (one per person)

---

## ⚠️ Important Notes

### Ngrok Limitations (Free Tier)
- URL changes every time you restart ngrok
- Need to update Railway variable each time
- Max 1 tunnel at a time

### Solutions:
1. **Ngrok Paid ($8/month):** Fixed URL, never changes
2. **Port Forwarding:** Free but requires router access
3. **Tailscale:** Free VPN, more secure

---

## 🆘 Troubleshooting

**Backend won't start:**
- Check Railway logs
- Verify environment variables
- Make sure requirements-deploy.txt is correct

**Camera not connecting:**
- Verify ngrok is running
- Check CAMERA_HTTP_URL is correct
- Test URL in browser first

**Frontend shows "Initializing...":**
- Backend might be sleeping (Railway free tier)
- Wait 30 seconds for it to wake up
- Check browser console for errors

---

## 🎉 You're Done!

Your system is now fully deployed and accessible from anywhere!

**Share with client:**
- Frontend URL: `https://camera-8cr2.vercel.app`
- They just need IP Webcam app
- No installation required!
