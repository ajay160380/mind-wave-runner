import cv2
import mediapipe as mp
import pygame

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self):
        success, image = self.cap.read()
        if not success:
            return False, False, None
            
        # Flip the image horizontally for a selfie-view display
        image = cv2.flip(image, 1)
        
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and find hands
        results = self.hands.process(image_rgb)
        
        is_jumping = False
        is_ducking = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the image for debugging
                self.mp_draw.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                wrist_y = hand_landmarks.landmark[0].y
                index_mcp_y = hand_landmarks.landmark[5].y
                index_tip_y = hand_landmarks.landmark[8].y
                
                # Jump Gesture: Open Hand / Index pointing up
                if index_tip_y < index_mcp_y - 0.1:
                    is_jumping = True
                
                # Duck Gesture: Hand closed (fist)
                elif index_tip_y > index_mcp_y:
                    is_ducking = True
                    
        # Convert the OpenCV image to a Pygame Surface for PiP display
        # First, convert OpenCV BGR to RGB
        image_pip_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Convert to Pygame Surface
        try:
            cam_surface = pygame.image.frombuffer(
                image_pip_rgb.tobytes(), 
                image_pip_rgb.shape[1::-1], 
                "RGB"
            )
            # Scale down to 160x120 for PiP
            cam_surface = pygame.transform.scale(cam_surface, (160, 120))
        except Exception:
            cam_surface = None
        
        return is_jumping, is_ducking, cam_surface
        
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

