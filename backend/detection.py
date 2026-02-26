import cv2
import numpy as np
import torch
from ultralytics import YOLO
import mediapipe as mp
from typing import Tuple, Optional
from collections import deque
import threading

# Patch torch.load to work with YOLOv8 models
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

class ActivityDetector:
    def __init__(self, confidence_threshold: float = 0.35):
        self.confidence_threshold = confidence_threshold
        
        # Initialize YOLO for person and phone detection - use small model for better distance detection
        self.yolo_model = YOLO('yolov8s.pt')  # Small model - better accuracy for distance
        
        # Initialize MediaPipe for pose estimation
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # Medium complexity for better distance detection
            min_detection_confidence=0.4,
            min_tracking_confidence=0.4
        )
        
        self.prev_frame = None
        self.frame_skip_counter = 0
        self.last_posture = None
        
        # Smoothing buffers for stable detection
        self.person_detection_buffer = deque(maxlen=5)
        self.phone_detection_buffer = deque(maxlen=5)
        self.posture_buffer = deque(maxlen=3)
        
        # Performance optimization
        self.detection_lock = threading.Lock()
    
    def detect_person_and_phone(self, frame) -> Tuple[bool, bool, Optional[list]]:
        """
        Detect person and phone in frame with improved distance detection
        Returns: (person_detected, phone_detected, person_bbox)
        """
        # Run YOLO with optimized settings for CCTV distance detection
        results = self.yolo_model(
            frame, 
            verbose=False, 
            imgsz=640,  # Higher resolution for better distance detection
            conf=self.confidence_threshold,
            iou=0.45,
            device='cpu',
            half=False
        )
        
        person_detected = False
        phone_detected = False
        person_bbox = None
        largest_person_area = 0
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Class 0 is person in COCO dataset
                if cls == 0:
                    bbox = box.xyxy[0].cpu().numpy()
                    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                    
                    # Track largest person (main subject)
                    if area > largest_person_area:
                        person_detected = True
                        person_bbox = bbox
                        largest_person_area = area
                
                # Class 67 is cell phone in COCO dataset
                if cls == 67 and conf > 0.3:  # Lower threshold for phone at distance
                    phone_detected = True
        
        # Smooth detection using buffer (reduce flickering)
        self.person_detection_buffer.append(person_detected)
        self.phone_detection_buffer.append(phone_detected)
        
        # Use majority voting for stable detection
        person_stable = sum(self.person_detection_buffer) >= 3
        phone_stable = sum(self.phone_detection_buffer) >= 3
        
        return person_stable, phone_stable, person_bbox
    
    def detect_posture(self, frame, person_bbox=None) -> Optional[str]:
        """
        Detect if person is sitting or standing using pose estimation
        Enhanced for distance detection
        Returns: 'sitting', 'standing', or None
        """
        # Skip posture detection every 3rd frame for performance
        self.frame_skip_counter += 1
        if self.frame_skip_counter % 3 != 0:
            return self.last_posture
        
        # Crop to person region if bbox available (improves accuracy at distance)
        if person_bbox is not None:
            x1, y1, x2, y2 = map(int, person_bbox)
            # Add padding
            padding = 20
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(frame.shape[1], x2 + padding)
            y2 = min(frame.shape[0], y2 + padding)
            frame = frame[y1:y2, x1:x2]
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            return self.last_posture
        
        landmarks = results.pose_landmarks.landmark
        
        # Get key points
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        
        # Calculate average positions
        hip_y = (left_hip.y + right_hip.y) / 2
        knee_y = (left_knee.y + right_knee.y) / 2
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        
        # Calculate torso angle
        torso_length = hip_y - shoulder_y
        knee_hip_distance = knee_y - hip_y
        
        # Enhanced heuristic for distance detection
        # Calculate visibility scores
        hip_visibility = (left_hip.visibility + right_hip.visibility) / 2
        knee_visibility = (left_knee.visibility + right_knee.visibility) / 2
        
        # Only make decision if landmarks are visible enough
        if hip_visibility < 0.5 or knee_visibility < 0.5:
            return self.last_posture
        
        # Improved sitting/standing detection
        if knee_hip_distance > torso_length * 0.6:
            current_posture = 'standing'
        else:
            current_posture = 'sitting'
        
        # Smooth posture changes
        self.posture_buffer.append(current_posture)
        
        # Use majority voting
        if len(self.posture_buffer) >= 2:
            posture_counts = {}
            for p in self.posture_buffer:
                posture_counts[p] = posture_counts.get(p, 0) + 1
            self.last_posture = max(posture_counts, key=posture_counts.get)
        else:
            self.last_posture = current_posture
        
        return self.last_posture
    
    def calculate_movement(self, frame) -> float:
        """
        Calculate movement level between frames
        Returns: movement score (0.0 to 1.0)
        """
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return 0.0
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate frame difference
        frame_diff = cv2.absdiff(self.prev_frame, gray_frame)
        
        # Threshold the difference
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        
        # Calculate percentage of changed pixels
        movement_score = np.sum(thresh) / (thresh.shape[0] * thresh.shape[1] * 255)
        
        self.prev_frame = gray_frame
        
        return min(movement_score * 10, 1.0)  # Normalize to 0-1
    
    def process_frame(self, frame) -> dict:
        """
        Process a single frame and return detection results
        Optimized for smooth performance
        """
        with self.detection_lock:
            person_detected, phone_detected, person_bbox = self.detect_person_and_phone(frame)
            
            posture = None
            if person_detected:
                posture = self.detect_posture(frame, person_bbox)
            
            movement_level = self.calculate_movement(frame)
            
            return {
                'person_detected': person_detected,
                'phone_detected': phone_detected,
                'posture': posture,
                'movement_level': movement_level,
                'person_bbox': person_bbox
            }
    
    def cleanup(self):
        """Release resources"""
        self.pose.close()
