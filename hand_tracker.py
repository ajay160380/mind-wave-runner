import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=1,
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self):
        success, image = self.cap.read()
        if not success: return False, False
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        is_jumping = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                wrist_y = hand_landmarks.landmark[0].y
                index_mcp_y = hand_landmarks.landmark[5].y
                index_tip_y = hand_landmarks.landmark[8].y
                
                if index_tip_y < index_mcp_y - 0.1:
                    is_jumping = True
                
        cv2.imshow("Hand Tracking (Debug)", image)
        cv2.waitKey(1)
        return is_jumping, False
        
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
