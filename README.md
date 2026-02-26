# Workplace Activity & Operational Efficiency Analytics System

An AI-powered MVP system for workplace activity monitoring using computer vision and pose estimation.

## Features

- Real-time person detection and tracking
- Posture detection (sitting/standing)
- Phone usage detection
- Activity classification (Active, Idle, Break, Phone Usage)
- Time tracking and analytics
- Live dashboard with charts
- SQLite database for activity logs

## Tech Stack

- **Backend**: Python, FastAPI, OpenCV, YOLOv8, MediaPipe
- **Frontend**: HTML, Tailwind CSS, Chart.js
- **Database**: SQLite

## Installation

1. Install Python dependencies:
```bash
cd workplace-ai
pip install -r requirements.txt
```

2. The system will automatically download YOLOv8 model on first run.

## Configuration

Edit `config.json` to customize:

- Camera source (webcam or RTSP stream)
- Detection thresholds
- Server ports
- Logging intervals

## Usage

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Open the dashboard:
```bash
cd frontend
# Open dashboard.html in your browser
# Or use a simple HTTP server:
python -m http.server 3000
```

3. Access the dashboard at `http://localhost:3000/dashboard.html`

## API Endpoints

- `GET /` - API status
- `GET /stats` - Current activity statistics
- `GET /logs?limit=100` - Recent activity logs
- `GET /video_feed` - Live video stream

## Activity States

- **Active**: Person present with movement detected
- **Idle**: Person present but minimal movement for >5 minutes
- **Phone Usage**: Person detected using phone
- **Break**: Person absent from frame for >2 minutes

## Privacy & Ethics

This system is designed for operational efficiency analytics only:
- No face recognition
- No identity tracking
- No audio recording
- Activity-based analytics only
- Single person tracking

## Project Structure

```
workplace-ai/
├── backend/
│   ├── main.py          # FastAPI server
│   ├── detection.py     # AI detection module
│   ├── tracking.py      # Time tracking engine
│   └── database.py      # SQLite database handler
├── frontend/
│   └── dashboard.html   # Web dashboard
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Future Enhancements

- Multi-camera support
- Multi-person tracking
- Cloud deployment
- Advanced analytics
- Export reports
- Mobile app

## License

MIT License
