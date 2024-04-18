import cv2
import os
import imutils
import time

from algorithms.humanDetector import HumanDetector

class Haarcascade(HumanDetector):
    def __init__(self, camera_id):
        HumanDetector.__init__(self, camera_id)

        # Initialize the Haar cascade classifiers for face and eye detection
        cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
        cascPatheyes = os.path.dirname(cv2.__file__) + "/data/haarcascade_eye_tree_eyeglasses.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPathface)
        self.eyeCascade = cv2.CascadeClassifier(cascPatheyes)
        self.isHumanDetected = False
        self.isOwnerDetected = False
        
    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()

        try:
            # Loop until the duration of the human detection loop has elapsed
            while (time.time() - start_time) < self.duration:
                # Capture frame-by-frame
                ret, src = self.cap.read()
        
                # Flip the frame vertically to correct the orientation
                frame = cv2.flip(src, 0)

                # Resize the frame to a smaller size to speed up the detection
                frame_resized = imutils.resize(frame, width=self.width, height = self.height)
                
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                # Detect faces in the frame using the Haar cascade classifier
                faces = self.faceCascade.detectMultiScale(gray,
                                                            scaleFactor=1.1,
                                                            minNeighbors=5,
                                                            minSize=(60, 60),
                                                            flags=cv2.CASCADE_SCALE_IMAGE)
                
                # Draw bounding boxes around the detected humans
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame_resized, (x, y), (x + w, y + h),(0,255,0), 2)
                    faceROI = frame_resized[y:y+h,x:x+w]
                    eyes = self.eyeCascade.detectMultiScale(faceROI)

                    # Draw bounding boxes around the detected eyes
                    for (x2, y2, w2, h2) in eyes:
                        eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
                        radius = int(round((w2 + h2) * 0.25))
                        frame_resized = cv2.circle(frame_resized, eye_center, radius, (255, 0, 0), 4)
                        self.isHumanDetected = True

                # Display the resulting frame
                cv2.imshow('Video', frame_resized)
                self.video.write(frame_resized)

                print(f"Human detected {self.isHumanDetected}")
                print(f"Owner detected {self.isOwnerDetected}")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
        finally:
            # Release the video capture device and close the image window when done
            self.cap.release()
            self.video.release()
            cv2.destroyAllWindows()
            if self.isHumanDetected:
                return True, None
            else: return False, None

if __name__ == "__main__":
    detector = Haarcascade(0)
    detector.detect_humans()
