import cv2

class HumanDetector:
    def __init__(self, camera_id):
        # Initialize the video capture device
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

        # Set the duration of the human detection loop in seconds
        self.duration = 30