import cv2
import imutils
import time
from datetime import datetime
from dhooks import Webhook, File

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
                    current_time = datetime.now()
                    current_time_image_format = current_time.strftime("%Y%m%d_%H%M%S")
                    human_detection_image_path = f"images/photo_{current_time_image_format}.jpg"
                    cv2.imwrite(human_detection_image_path, image)
                        
                    self.cap.release()
                    cv2.destroyAllWindows()
                    
                    # Create a Webhook object and pass in the URL of the Discord webhook
                    hook = Webhook("https://discord.com/api/webhooks/1090684363714351144/NMGFwquH-LvDjJBHL8SmxQtKRjFjT8ZQ6Nqb-r8IMZP7fkqLJHylMijY1J8FRv4zH3Us")

                    dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")

                    data = f"Attention! Our sensors have detected the presence of a human being as of {dt_string}.\nFor safety reasons, please stand still and wait for further instructions."
                    human_detection_image = File(human_detection_image_path)
                    
                    hook.send(data, file=human_detection_image)
                
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
