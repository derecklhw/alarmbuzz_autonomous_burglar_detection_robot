import os
import glob
import numpy as np
import cv2
import imutils
import time

from algorithms.humanDetector import HumanDetector

class Yunet(HumanDetector):
    def __init__(self, camera_id):
        HumanDetector.__init__(self, camera_id)

        # Initialize the Yunet model for face detection
        weights = os.path.join(os.path.dirname(__file__), "face_detection_yunet_2023mar.onnx")
        self.face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))

        # Initialize the SFace model for face recognition
        weights = os.path.join(os.path.dirname(__file__), "face_recognition_sface_2021dec.onnx")
        self.face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        self.COSINE_THRESHOLD = 0.363
        self.NORML2_THRESHOLD = 1.128

        self.dictionary = []
        self.load_features()

        self.isHumanDetected = False
        self.isOwnerDetected = False

    def load_features(self):
        # Load the features from the files
        files = glob.glob(os.path.join(os.path.dirname(__file__), "*.npy"))
        for file in files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0]
            self.dictionary.append((user_id, feature))

    def match(self, feature1):
        for element in self.dictionary:
            user_id, feature2 = element
            score = self.face_recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > self.COSINE_THRESHOLD:
                return True, (user_id, score)
            return False, ("", 0.0)
    
    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()
        try:
            while (time.time() - start_time) < self.duration:
                # Capture frame-by-frame
                ret, src = self.cap.read()
                
                # Flip the frame vertically to correct the orientation
                frame = cv2.flip(src, 0)

                # Resize the frame to a smaller size to speed up the detection
                frame_resized = imutils.resize(frame, width=self.width, height = self.height)

                # If the image is not in 3 channels, convert it to 3 channels.
                channels = 1 if len(frame_resized.shape) == 2 else frame_resized.shape[2]
                if channels == 1:
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_GRAY2BGR)
                if channels == 4:
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGRA2BGR)

                # Specify the input size.
                height, width, _ = frame_resized.shape
                self.face_detector.setInputSize((width, height))

                if ret:
                    # Detect faces.
                    result, faces = self.face_detector.detect(frame_resized)
                    faces = faces if faces is not None else []

                    for face in faces:
                        self.isHumanDetected = True
                        # Crop the face and extract features.
                        aligned_face = self.face_recognizer.alignCrop(frame_resized, face)
                        feature = self.face_recognizer.feature(aligned_face)

                        # Match with the dictionary.
                        result, user = self.match(feature)

                        # Draw the bounding box around the face.
                        box = list(map(int, face[:4]))
                        color = (0, 255, 0) if result else (0, 0, 255)
                        thickness = 2
                        cv2.rectangle(frame_resized, box, color, thickness, cv2.LINE_AA)

                        # Draw the recognition result.
                        id, score = user if result else ("unknown", 0.0)
                        text = "{0} ({1:.2f})".format(id, score)
                        position = (box[0], box[1] - 10)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        scale = 0.6
                        cv2.putText(
                            frame_resized, text, position, font, scale, color, thickness, cv2.LINE_AA
                        )

                        if (result):
                            self.isOwnerDetected = True
                            break
                    
                    if (self.isOwnerDetected):
                        break
                    
                    # Display the image.
                    cv2.imshow("Video", frame_resized)
                    self.video.write(frame_resized)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                else:
                    break

        finally:
            self.cap.release()
            self.video.release()
            cv2.destroyAllWindows()

            return self.isHumanDetected, self.isOwnerDetected

if __name__ == "__main__":
    detector = Yunet(0)
    detector.detect_humans()
