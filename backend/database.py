import sqlite3
from datetime import datetime
from typing import List, Dict
import json

class Database:
    """In-memory database - no persistence"""
    def __init__(self):
        self.activity_logs = []
        self.max_logs = 1000  # Keep last 1000 logs in memory
        print("✓ Using in-memory storage (no database)")
    
    def log_activity(self, status: str, present: bool, posture: str = None, 
                     phone_usage: bool = False, movement_level: float = 0.0):
        """Log activity snapshot in memory"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'status': status,
            'present': present,
            'posture': posture,
            'phone_usage': phone_usage,
            'movement_level': movement_level
        }
        
        self.activity_logs.append(log_entry)
        
        # Keep only last max_logs entries
        if len(self.activity_logs) > self.max_logs:
            self.activity_logs.pop(0)
    
    def update_time_summary(self, present_time: int, active_time: int, idle_time: int,
                           phone_usage_time: int, break_time: int):
        """No-op for in-memory mode"""
        pass
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent activity logs from memory"""
        return self.activity_logs[-limit:][::-1]  # Return last N logs, reversed
    
    def get_today_summary(self) -> Dict:
        """Get today's time summary (not used in stateless mode)"""
        return {
            'present_time': 0,
            'active_time': 0,
            'idle_time': 0,
            'phone_usage_time': 0,
            'break_time': 0
        }
