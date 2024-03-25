import cv2
import imutils
import time
from utils import Utils

class HumanDetector:
    def __init__(self, camera_id):
        # Initialize the HOG descriptor with the default people detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Initialize the video capture device
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

        # Set the duration of the human detection loop in seconds
        self.duration = 20
        
    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()

        # Loop until the duration of the human detection loop has elapsed
        while (time.time() - start_time) < self.duration:
            # Read a frame from the video capture device
            ret, src = self.cap.read()

            # Flip the frame vertically to correct the orientation
            image = cv2.flip(src, 0)

            if ret:
                # Resize the frame to a smaller size to speed up the detection
                image = imutils.resize(image, 
                                       width=min(400, image.shape[1]))

                # Detect humans in the frame using the HOG descriptor
                (regions, _) = self.hog.detectMultiScale(image,
                                                          winStride=(4, 4),
                                                          padding=(4, 4),
                                                          scale=1.05)

                # If humans are detected, take a photo and send a notification to Discord
                for (x, y, w, h) in regions:
                    cv2.rectangle(image, (x, y),
                                  (x + w, y + h), 
                                  (0, 0, 255), 2)

                    utils = Utils()
                    utils.saveImage(image)     
                    utils.sendDiscordNotification()

                    print("AlarmBuzz has detected a human presence! Please check your surroundings.\n")

                    # Release the video capture device and close the image window
                    self.cap.release()
                    cv2.destroyAllWindows()

                    return True

                # Display the image with bounding boxes around detected humans
                cv2.imshow("Image", image)

                # Wait for a key press and exit the loop if the 'q' key is pressed
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release the video capture device and close the image window when done
        self.cap.release()
        cv2.destroyAllWindows()

        return False

if __name__ == "__main__":
    # Create a HumanDetector object with the default camera ID (0)
    detector = HumanDetector(0)
    detector.detect_humans()
