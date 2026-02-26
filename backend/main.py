import cv2
import json
import time
import threading
import numpy as np
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from detection import ActivityDetector
from tracking import ActivityTracker
from database import Database

# Load configuration
with open('../config.json', 'r') as f:
    config = json.load(f)

# Initialize components
app = FastAPI(title="Workplace Activity Analytics API")
detector = ActivityDetector(confidence_threshold=config['detection']['confidence_threshold'])
tracker = ActivityTracker(
    idle_threshold=config['detection']['idle_threshold_seconds'],
    break_threshold=config['detection']['break_threshold_seconds']
)
db = Database()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
camera = None
latest_frame = None
is_running = False

def init_camera():
    """Initialize camera based on config"""
    global camera
    
    source = config['camera']['source']
    
    if source == 'webcam':
        camera = cv2.VideoCapture(config['camera']['webcam_index'])
    elif source == 'http':
        # HTTP stream from phone
        camera = cv2.VideoCapture(config['camera']['http_url'])
    elif source == 'rtsp':
        # RTSP stream (better performance)
        camera = cv2.VideoCapture(config['camera']['rtsp_url'])
    else:
        # Default to webcam
        camera = cv2.VideoCapture(0)
    
    # Set camera properties for better performance
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    if not camera.isOpened():
        raise Exception(f"Failed to open camera with source: {source}")
    
    return camera

def process_video_stream():
    """Main video processing loop - Ultra optimized"""
    global latest_frame, is_running
    
    last_log_time = time.time()
    log_interval = config['detection']['log_interval_seconds']
    
    # Adaptive resolution for CCTV
    target_width = 960  # Higher resolution for better distance detection
    
    # Frame buffer for smooth streaming
    frame_buffer = []
    
    while is_running:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.05)
            continue
        
        # Enhance frame quality for distance detection
        height, width = frame.shape[:2]
        
        # Maintain aspect ratio
        if width > target_width:
            scale = target_width / width
            frame = cv2.resize(frame, (target_width, int(height * scale)), 
                             interpolation=cv2.INTER_LINEAR)
        
        # Apply sharpening for better distance detection
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        frame = cv2.filter2D(frame, -1, kernel)
        
        # Process frame
        detection_result = detector.process_frame(frame)
        
        # Update tracking
        status = tracker.update(detection_result)
        
        # Draw enhanced annotations
        annotated_frame = frame.copy()
        
        # Draw bounding box if person detected
        if detection_result['person_bbox'] is not None:
            bbox = detection_result['person_bbox']
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Status indicator with background
        status_color = {
            'active': (0, 255, 0),
            'idle': (0, 255, 255),
            'phone_usage': (0, 0, 255),
            'break': (128, 0, 128)
        }.get(status, (128, 128, 128))
        
        cv2.rectangle(annotated_frame, (5, 5), (300, 160), (0, 0, 0), -1)
        cv2.rectangle(annotated_frame, (5, 5), (300, 160), status_color, 2)
        
        cv2.putText(annotated_frame, f"Status: {status.upper()}", (15, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        if detection_result['person_detected']:
            cv2.putText(annotated_frame, "Person: DETECTED", (15, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if detection_result['posture']:
                cv2.putText(annotated_frame, f"Posture: {detection_result['posture'].upper()}", 
                           (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(annotated_frame, "Person: NOT DETECTED", (15, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        if detection_result['phone_detected']:
            cv2.putText(annotated_frame, "Phone: IN USE", (15, 130),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Encode frame with better quality for CCTV
        _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        latest_frame = buffer
        
        # Log to database periodically
        current_time = time.time()
        if current_time - last_log_time >= log_interval:
            db.log_activity(
                status=status,
                present=detection_result['person_detected'],
                posture=detection_result['posture'],
                phone_usage=detection_result['phone_detected'],
                movement_level=detection_result['movement_level']
            )
            
            # Update time summary
            stats = tracker.get_stats()
            db.update_time_summary(
                present_time=stats['present_time'],
                active_time=stats['active_time'],
                idle_time=stats['idle_time'],
                phone_usage_time=stats['phone_usage_time'],
                break_time=stats['break_time']
            )
            
            last_log_time = current_time
        
        time.sleep(0.033)  # ~30 FPS for smooth video

def generate_frames():
    """Generate frames for video streaming - optimized"""
    while True:
        if latest_frame is not None:
            frame = latest_frame.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.033)  # 30 FPS

@app.on_event("startup")
async def startup_event():
    """Start video processing on server startup"""
    global is_running
    
    init_camera()
    is_running = True
    
    # Start video processing in background thread
    thread = threading.Thread(target=process_video_stream, daemon=True)
    thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    global is_running
    
    is_running = False
    if camera:
        camera.release()
    detector.cleanup()

@app.get("/")
async def root():
    return {"message": "Workplace Activity Analytics API", "status": "running"}

@app.get("/stats")
async def get_stats():
    """Get current activity statistics"""
    stats = tracker.get_stats()
    
    # Format times for display
    stats['present_time_formatted'] = tracker.format_time(stats['present_time'])
    stats['active_time_formatted'] = tracker.format_time(stats['active_time'])
    stats['idle_time_formatted'] = tracker.format_time(stats['idle_time'])
    stats['phone_usage_time_formatted'] = tracker.format_time(stats['phone_usage_time'])
    stats['break_time_formatted'] = tracker.format_time(stats['break_time'])
    
    return stats

@app.get("/logs")
async def get_logs(limit: int = 100):
    """Get recent activity logs"""
    logs = db.get_recent_logs(limit)
    return {"logs": logs, "count": len(logs)}

@app.get("/video_feed")
async def video_feed():
    """Stream video feed"""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config['server']['host'],
        port=config['server']['port']
    )
