import os
import sys
import glob
import numpy as np
import cv2

COSINE_THRESHOLD = 0.363
NORML2_THRESHOLD = 1.128


# Function to compare features with a dictionary and return matched user and score
def match(recognizer, feature1, dictionary):
    for element in dictionary:
        user_id, feature2 = element
        score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
        print(score)
        if score > COSINE_THRESHOLD:
            return True, (user_id, score)
    return False, ("", 0.0)


def main():
    # Open the capture
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "49.jpg"))  # Image file
    # capture = cv2.VideoCapture(0)  # Camera
    if not capture.isOpened():
        exit()

    # Load features
    dictionary = []
    files = glob.glob(os.path.join(directory, "*.npy"))
    for file in files:
        feature = np.load(file)
        user_id = os.path.splitext(os.path.basename(file))[0]
        dictionary.append((user_id, feature))

    # Load the model
    weights = os.path.join(directory, "face_detection_yunet_2023mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    weights = os.path.join(directory, "face_recognition_sface_2021dec.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    while True:
        # Capture a frame and read the image
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        # Convert the image to 3 channels if it is not already
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if channels == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Specify the input size
        height, width, _ = image.shape
        face_detector.setInputSize((width, height))

        # Detect faces
        result, faces = face_detector.detect(image)
        faces = faces if faces is not None else []

        for face in faces:
            # Crop the face and extract features
            aligned_face = face_recognizer.alignCrop(image, face)
            feature = face_recognizer.feature(aligned_face)

            # Match against the dictionary
            result, user = match(face_recognizer, feature, dictionary)

            # Draw the bounding box for the face
            box = list(map(int, face[:4]))
            color = (0, 255, 0) if result else (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

            # Display the recognition result
            id, score = user if result else ("unknown", 0.0)
            text = "{0} ({1:.2f})".format(id, score)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.6
            cv2.putText(
                image, text, position, font, scale, color, thickness, cv2.LINE_AA
            )

        # Display the image
        cv2.imshow("face recognition", image)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
