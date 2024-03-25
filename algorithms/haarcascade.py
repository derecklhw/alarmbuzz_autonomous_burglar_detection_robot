import cv2
import os
import time

class HumanDetector:
    def __init__(self, camera_id):
        cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
        cascPatheyes = os.path.dirname(cv2.__file__) + "/data/haarcascade_eye_tree_eyeglasses.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPathface)
        self.eyeCascade = cv2.CascadeClassifier(cascPatheyes)
        self.video_capture = cv2.VideoCapture(0)
        self.duration = 30


    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()

        # Loop until the duration of the human detection loop has elapsed
        while (time.time() - start_time) < self.duration:
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()
    
            # Flip the frame
            frame = cv2.flip(frame, 0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if ret: 
                faces = self.faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
                    faceROI = frame[y:y+h,x:x+w]
                    eyes = self.eyeCascade.detectMultiScale(faceROI)
                    for (x2, y2, w2, h2) in eyes:
                        eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
                        radius = int(round((w2 + h2) * 0.25))
                        frame = cv2.circle(frame, eye_center, radius, (255, 0, 0), 4)

                        self.video_capture.release()
                        cv2.destroyAllWindows()

                        return True, frame

                # Display the resulting frame
                cv2.imshow('Video', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        self.video_capture.release()
        cv2.destroyAllWindows()

        return False, None

if __name__ == "__main__":
    detector = HumanDetector(0)
    detector.detect_humans()
