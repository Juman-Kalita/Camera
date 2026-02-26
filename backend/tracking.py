import time
from datetime import datetime
from typing import Dict

class ActivityTracker:
    def __init__(self, idle_threshold: int = 300, break_threshold: int = 120):
        self.idle_threshold = idle_threshold  # seconds
        self.break_threshold = break_threshold  # seconds
        
        # Time tracking
        self.present_time = 0
        self.active_time = 0
        self.idle_time = 0
        self.phone_usage_time = 0
        self.break_time = 0
        
        # State tracking
        self.current_status = 'break'
        self.last_update = time.time()
        self.last_movement_time = time.time()
        self.last_present_time = time.time()
        self.phone_usage_start = None
        
        # Session tracking
        self.session_start = datetime.now()
    
    def update(self, detection_result: dict) -> str:
        """
        Update tracking based on detection results
        Returns: current status
        """
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        person_detected = detection_result['person_detected']
        phone_detected = detection_result['phone_detected']
        movement_level = detection_result['movement_level']
        
        # Determine current status
        if not person_detected:
            # Person not in frame
            time_away = current_time - self.last_present_time
            
            if time_away > self.break_threshold:
                self.current_status = 'break'
                self.break_time += elapsed
            else:
                # Short absence, still count as present
                self.present_time += elapsed
        else:
            # Person is present
            self.present_time += elapsed
            self.last_present_time = current_time
            
            # Check for phone usage
            if phone_detected:
                self.current_status = 'phone_usage'
                self.phone_usage_time += elapsed
                if self.phone_usage_start is None:
                    self.phone_usage_start = current_time
            else:
                self.phone_usage_start = None
                
                # Check for idle vs active
                if movement_level > 0.1:
                    self.current_status = 'active'
                    self.active_time += elapsed
                    self.last_movement_time = current_time
                else:
                    time_since_movement = current_time - self.last_movement_time
                    
                    if time_since_movement > self.idle_threshold:
                        self.current_status = 'idle'
                        self.idle_time += elapsed
                    else:
                        self.current_status = 'active'
                        self.active_time += elapsed
        
        self.last_update = current_time
        return self.current_status
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return {
            'present_time': int(self.present_time),
            'active_time': int(self.active_time),
            'idle_time': int(self.idle_time),
            'phone_usage_time': int(self.phone_usage_time),
            'break_time': int(self.break_time),
            'current_status': self.current_status,
            'session_start': self.session_start.isoformat()
        }
    
    def reset_daily(self):
        """Reset counters for new day"""
        self.present_time = 0
        self.active_time = 0
        self.idle_time = 0
        self.phone_usage_time = 0
        self.break_time = 0
        self.session_start = datetime.now()
    
    def format_time(self, seconds: int) -> str:
        """Format seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
