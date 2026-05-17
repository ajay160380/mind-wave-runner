import cv2

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def process_frame(self):
        success, image = self.cap.read()
        if not success:
            return False, False
        image = cv2.flip(image, 1)
        return False, False
        
    def release(self):
        self.cap.release()
