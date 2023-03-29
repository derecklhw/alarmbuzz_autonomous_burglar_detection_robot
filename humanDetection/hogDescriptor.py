import cv2
import imutils
import time
from datetime import datetime

class HumanDetector:
    def __init__(self, camera_id):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
        self.duration = 20
        
    def detect_humans(self):
        start_time = time.time()
        while (time.time() - start_time) < self.duration:
            ret, src = self.cap.read()
            image = cv2.flip(src, 0)
            if ret:
                image = imutils.resize(image, 
                                       width=min(400, image.shape[1]))
                (regions, _) = self.hog.detectMultiScale(image,
                                                          winStride=(4, 4),
                                                          padding=(4, 4),
                                                          scale=1.05)
                for (x, y, w, h) in regions:
                    cv2.rectangle(image, (x, y),
                                  (x + w, y + h), 
                                  (0, 0, 255), 2)
                    # Take a photo when humans are detected
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    cv2.imwrite(f"images/photo_{current_time}.jpg", image)

                    self.cap.release()
                    cv2.destroyAllWindows()
                    return True
                cv2.imshow("Image", image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = HumanDetector(0)  # camera_id = 0 for default camera
    detector.detect_humans()
