import cv2

class HumanDetector:
    def __init__(self, camera_id):
        # Initialize the video capture device
        self.width = 640
        self.height = 480
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
        self.video = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 25, (self.width, self.height))

        # Set the duration of the human detection loop in seconds
        self.duration = 30