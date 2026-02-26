# 🚀 Client Setup Guide - Workplace Activity Analytics

## For End Users (Non-Technical)

This guide will help you set up the workplace activity monitoring system on your computer in **under 10 minutes**.

---

## 📋 What You Need

- Windows, Mac, or Linux computer
- Webcam (built-in or external)
- Internet connection
- 15 minutes of your time

---

## 🎯 Step-by-Step Installation

### Step 1: Install Python (5 minutes)

**Windows:**
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.12"
3. Run the installer
4. ✅ **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

**Mac:**
1. Open Terminal (search for "Terminal" in Spotlight)
2. Install Homebrew (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.12
   ```

**Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3-pip
```

### Step 2: Download the Code (2 minutes)

**Option A: Using Git (Recommended)**
1. Install Git: https://git-scm.com/downloads
2. Open Terminal/Command Prompt
3. Run:
   ```bash
   git clone https://github.com/Juman-Kalita/Camera.git
   cd Camera
   ```

**Option B: Download ZIP**
1. Go to https://github.com/Juman-Kalita/Camera
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file
5. Open Terminal/Command Prompt in that folder

### Step 3: Install Dependencies (3 minutes)

Open Terminal/Command Prompt in the `Camera` folder and run:

**Windows:**
```bash
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

This will download all necessary AI models and libraries. It may take 2-3 minutes.

### Step 4: Start the System (1 minute)

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**OR manually:**
```bash
# Terminal 1 - Start Backend
cd backend
python main.py

# Terminal 2 - Start Frontend (open new terminal)
cd frontend
python -m http.server 3000
```

### Step 5: Open Dashboard

Your browser should automatically open to:
```
http://localhost:3000/dashboard.html
```

If not, manually open that URL in your browser.

---

## ✅ What You Should See

1. **Live Camera Feed** - Your webcam video with AI annotations
2. **Stats Cards** - Time tracking (Presence, Active, Idle, Phone, Break)
3. **Current Status** - Real-time activity status
4. **Charts** - Activity distribution and timeline
5. **Activity Logs** - Recent activity history

---

## 🎮 How to Use

### Daily Usage

1. **Start Your Day:**
   - Run `start.bat` (Windows) or `./start.sh` (Mac/Linux)
   - Dashboard opens automatically
   - System starts monitoring

2. **During Work:**
   - Keep the system running in background
   - Dashboard shows real-time stats
   - AI detects: presence, posture, phone usage

3. **End Your Day:**
   - Close the terminal windows
   - Or press `Ctrl+C` in terminal

### Understanding the Stats

- **Total Presence:** Time you're in front of camera
- **Active Time:** Time with movement detected
- **Idle Time:** Time present but no movement (>5 min)
- **Phone Usage:** Time detected using phone
- **Break Time:** Time away from camera (>2 min)

### Activity States

- 🟢 **Active:** Person present + moving
- 🟡 **Idle:** Person present but no movement
- 🔴 **Phone Usage:** Person detected using phone
- 🟣 **Break:** Person away from camera

---

## 🔧 Troubleshooting

### Camera Not Working

**Problem:** Black screen or "Camera not found"

**Solutions:**
1. Check if another app is using the camera (Zoom, Teams, etc.)
2. Grant camera permissions:
   - **Windows:** Settings → Privacy → Camera
   - **Mac:** System Preferences → Security & Privacy → Camera
3. Try different camera index in `config.json`:
   ```json
   "webcam_index": 1
   ```

### Dependencies Failed to Install

**Problem:** Error during `pip install`

**Solutions:**
1. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Install Visual C++ Build Tools (Windows):
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
3. Try installing one by one:
   ```bash
   pip install fastapi
   pip install uvicorn
   pip install opencv-python
   pip install ultralytics
   pip install mediapipe
   ```

### Port Already in Use

**Problem:** "Port 8000 already in use"

**Solutions:**
1. Close other applications using port 8000
2. Or change port in `config.json`:
   ```json
   "port": 8001
   ```

### Slow Performance

**Problem:** Laggy video or slow detection

**Solutions:**
1. Close other heavy applications
2. Reduce video quality in `config.json`:
   ```json
   "confidence_threshold": 0.4
   ```
3. Upgrade your computer's RAM

---

## 📱 Using Phone Camera Instead

If you want to use your phone camera instead of laptop webcam:

1. **Install IP Webcam App:**
   - Android: https://play.google.com/store/apps/details?id=com.pas.webcam
   - iOS: Use "EpocCam" or similar

2. **Start IP Webcam:**
   - Open app
   - Click "Start Server"
   - Note the IP address (e.g., `http://192.168.1.100:8080`)

3. **Update Config:**
   - Open `config.json`
   - Change:
     ```json
     "source": "http",
     "http_url": "http://YOUR_PHONE_IP:8080/video"
     ```

4. **Restart System**

---

## 🔒 Privacy & Security

### What Data is Collected?

- ✅ Activity timestamps
- ✅ Presence status
- ✅ Posture (sitting/standing)
- ✅ Phone usage detection
- ✅ Movement levels

### What is NOT Collected?

- ❌ No face recognition
- ❌ No identity tracking
- ❌ No video recording
- ❌ No audio recording
- ❌ No screenshots

### Where is Data Stored?

- All data stored **locally** on your computer
- In-memory storage (resets when you close the app)
- No cloud upload
- No external servers

### Can My Employer See My Data?

- **No**, unless you share your screen
- Data stays on your machine
- You have full control

---

## 📊 Accessing from Other Devices

### View Dashboard on Phone/Tablet

1. Find your computer's local IP:
   - **Windows:** `ipconfig` (look for IPv4)
   - **Mac/Linux:** `ifconfig` (look for inet)

2. On your phone/tablet, open browser:
   ```
   http://YOUR_COMPUTER_IP:3000/dashboard.html
   ```

3. Make sure both devices are on same WiFi

---

## 🆘 Getting Help

### Common Issues

1. **"Python not found"**
   - Reinstall Python with "Add to PATH" checked

2. **"Module not found"**
   - Run: `pip install -r requirements.txt` again

3. **"Camera permission denied"**
   - Check system privacy settings

4. **"Connection refused"**
   - Make sure backend is running
   - Check if port 8000 is available

### Still Need Help?

- Check GitHub Issues: https://github.com/Juman-Kalita/Camera/issues
- Contact support: [your-email@example.com]
- Read full documentation: `README.md`

---

## 🎓 Advanced Configuration

### Customize Detection Settings

Edit `config.json`:

```json
{
  "detection": {
    "idle_threshold_seconds": 300,      // 5 minutes
    "break_threshold_seconds": 120,     // 2 minutes
    "log_interval_seconds": 30,         // Log every 30 sec
    "confidence_threshold": 0.35        // AI confidence
  }
}
```

### Change Server Ports

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "frontend": {
    "port": 3000
  }
}
```

---

## 📝 System Requirements

### Minimum:
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Storage: 2 GB free space
- Webcam: 720p
- OS: Windows 10, macOS 10.14, Ubuntu 18.04

### Recommended:
- CPU: Quad-core 2.5 GHz
- RAM: 8 GB
- Storage: 5 GB free space
- Webcam: 1080p
- OS: Windows 11, macOS 12+, Ubuntu 20.04+

---

## 🔄 Updating the System

### Get Latest Version

**Using Git:**
```bash
cd Camera
git pull
pip install -r requirements.txt
```

**Manual:**
1. Download latest ZIP from GitHub
2. Extract and replace old files
3. Run `pip install -r requirements.txt`

---

## ✨ Tips for Best Results

1. **Good Lighting:** Ensure your face is well-lit
2. **Stable Position:** Keep camera at eye level
3. **Clear Background:** Minimize distractions behind you
4. **Regular Breaks:** System tracks breaks automatically
5. **Close Unused Apps:** For better performance

---

## 🎉 You're All Set!

The system is now running and monitoring your workplace activity. 

**Remember:**
- This is for YOUR benefit, not surveillance
- You control all the data
- You can stop it anytime
- It helps you understand your work patterns

Enjoy better productivity insights! 🚀
