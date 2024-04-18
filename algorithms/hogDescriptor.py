import cv2
import imutils
import time

from algorithms.humanDetector import HumanDetector

class HogDescriptor(HumanDetector):
    def __init__(self, camera_id):
        HumanDetector.__init__(self, camera_id)

        # Initialize the HOG descriptor with the default people detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.isHumanDetected = False
        self.isOwnerDetected = False
        
    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()

        try:
            # Loop until the duration of the human detection loop has elapsed
            while (time.time() - start_time) < self.duration:
                # Read a frame from the video capture device
                ret, src = self.cap.read()

                # Flip the frame vertically to correct the orientation
                frame = cv2.flip(src, 0)

                # Resize the frame to a smaller size to speed up the detection
                frame_resized = imutils.resize(frame, width=self.width, height=self.height)

                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

                if ret:
                    # Detect humans in the frame using the HOG descriptor
                    (regions, _) = self.hog.detectMultiScale(gray,
                                                            winStride=(4, 4),
                                                            padding=(4, 4),
                                                            scale=1.05)

                    # Draw bounding boxes around the detected humans
                    for (x, y, w, h) in regions:
                        cv2.rectangle(frame_resized, (x, y),
                                    (x + w, y + h), 
                                    (0, 0, 255), 2)
                        self.isHumanDetected = True

                    # Display the image with bounding boxes around detected humans
                    cv2.imshow("Video", frame_resized)
                    self.video.write(frame_resized)

                    # Wait for a key press and exit the loop if the 'q' key is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
        finally:
            # Release the video capture device and close the image window when done
            self.cap.release()
            self.video.release()
            cv2.destroyAllWindows()
            if self.isHumanDetected and not self.isOwnerDetected:
                return True, False
            else: return False, False

if __name__ == "__main__":
    # Create a HumanDetector object with the default camera ID (0)
    detector = HogDescriptor(0)
    detector.detect_humans()
