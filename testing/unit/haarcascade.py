import numpy as np
import cv2
import os

# Path setup for using OpenCV's pre-trained Haar cascades
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
cascPatheyes = (
    os.path.dirname(cv2.__file__) + "/data/haarcascade_eye_tree_eyeglasses.xml"
)

# Create the Haar cascade classifiers for face and eyes detection
face_detector = cv2.CascadeClassifier(cascPathface)
eye_detector = cv2.CascadeClassifier(cascPatheyes)

# Load an image from disk and convert it to grayscale
img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces_result = face_detector.detectMultiScale(gray, 1.3, 5)
for x, y, w, h in faces_result:
    # Draw a rectangle around each face
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Region of interest (ROI) in grayscale and color for further analysis within the face bounding box
    roi_gray = gray[y : y + h, x : x + w]
    roi_color = img[y : y + h, x : x + w]

    # Detect eyes within the face region
    eyes = eye_detector.detectMultiScale(roi_gray)
    for ex, ey, ew, eh in eyes:
        # Draw a rectangle around each eye within the face
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

# Display the resulting frame
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
