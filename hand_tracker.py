import pygame
import threading
import time
import math
from settings import resource_path

try:
    import cv2
    import mediapipe as mp
    CAMERA_CV_AVAILABLE = True
except ImportError:
    CAMERA_CV_AVAILABLE = False

class HandTracker:
    def __init__(self):
        # Thread-safe synchronization variables
        self.lock = threading.Lock()
        self.is_jumping = False
        self.is_ducking = False
        self.cam_surface = None
        self.running = True
        
        if not CAMERA_CV_AVAILABLE:
            print("Webcam CV/MediaPipe libraries not available. Keyboard-only mode activated.")
            self.cap = None
            self.landmarker = None
            return

        # Open default webcam capture
        self.cap = cv2.VideoCapture(0)
        
        # Modern Google MediaPipe HandLandmarker Tasks API
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=resource_path('hand_landmarker.task')),
            running_mode=VisionRunningMode.IMAGE
        )
        self.landmarker = HandLandmarker.create_from_options(options)
        
        # Hand connections outline (21 bones)
        self.HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]
        
        # Start dedicated background thread
        self.thread = threading.Thread(target=self._background_loop, daemon=True)
        self.thread.start()

    def _dist_2d(self, p1, p2):
        # Extremely stable 2D screen distance (removes noisy 3D depth fluctuations)
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def _background_loop(self):
        # Dedicated loop for the webcam capture and MediaPipe inference
        while self.running:
            success, image = self.cap.read()
            if not success:
                time.sleep(0.01)
                continue
                
            # Flip the image horizontally for a selfie-view display
            image = cv2.flip(image, 1)
            h, w, c = image.shape
            
            # Convert BGR image to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Create MediaPipe Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            
            # Run detection
            results = self.landmarker.detect(mp_image)
            
            is_jumping = False
            is_ducking = False
            
            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    # Convert normalized landmarks to pixel coordinates
                    points = []
                    for lm in hand_landmarks:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        points.append((cx, cy))
                    
                    # Draw Emerald tracking lines (Green: BGR 80, 200, 0)
                    for connection in self.HAND_CONNECTIONS:
                        if connection[0] < len(points) and connection[1] < len(points):
                            p1 = points[connection[0]]
                            p2 = points[connection[1]]
                            cv2.line(image, p1, p2, (80, 200, 0), 2)
                    
                    # Draw joint circles (White-capped Green: BGR 255, 255, 255)
                    for pt in points:
                        cv2.circle(image, pt, 4, (255, 255, 255), -1)
                        cv2.circle(image, pt, 2, (40, 160, 0), -1)
                    
                    # ------------------ PURE WRIST-RELATIVE 2D PALM DECODER ------------------
                    if len(hand_landmarks) >= 21:
                        wrist = hand_landmarks[0]
                        extended_fingers = 0
                        
                        # Compare tip-to-wrist distance vs PIP-to-wrist distance
                        # Index (Tip: 8, PIP: 6)
                        if self._dist_2d(hand_landmarks[8], wrist) > self._dist_2d(hand_landmarks[6], wrist):
                            extended_fingers += 1
                        # Middle (Tip: 12, PIP: 10)
                        if self._dist_2d(hand_landmarks[12], wrist) > self._dist_2d(hand_landmarks[10], wrist):
                            extended_fingers += 1
                        # Ring (Tip: 16, PIP: 14)
                        if self._dist_2d(hand_landmarks[16], wrist) > self._dist_2d(hand_landmarks[14], wrist):
                            extended_fingers += 1
                        # Pinky (Tip: 20, PIP: 18)
                        if self._dist_2d(hand_landmarks[20], wrist) > self._dist_2d(hand_landmarks[18], wrist):
                            extended_fingers += 1
                        
                        # --- GESTURE CLASSIFIER ---
                        # 1. Palm Open (>= 3 extended fingers) ➔ JUMP!
                        if extended_fingers >= 3:
                            is_jumping = True
                        # 2. Palm Closed / Fist (<= 1 extended finger) ➔ DUCK/SLIDE!
                        elif extended_fingers <= 1:
                            is_ducking = True
                            
            # Convert the OpenCV image to a Pygame Surface for PiP display
            image_pip_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            try:
                cam_surface = pygame.image.frombuffer(
                    image_pip_rgb.tobytes(), 
                    image_pip_rgb.shape[1::-1], 
                    "RGB"
                )
                cam_surface = pygame.transform.scale(cam_surface, (160, 120))
            except Exception:
                cam_surface = None
                
            # Thread-safe writing
            with self.lock:
                self.is_jumping = is_jumping
                self.is_ducking = is_ducking
                self.cam_surface = cam_surface
                
            # Prevent thread from spinning too fast
            time.sleep(0.005)

    def process_frame(self):
        # Non-blocking, instantaneous read
        with self.lock:
            return self.is_jumping, self.is_ducking, self.cam_surface

    def release(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
