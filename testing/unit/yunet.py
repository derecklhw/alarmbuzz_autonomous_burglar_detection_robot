import os
import numpy as np
import cv2


def main():
    # Open the capture
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "test.jpg"))  # Image file
    # capture = cv2.VideoCapture(0)  # Camera
    if not capture.isOpened():
        exit()

    # Load the model
    weights = os.path.join(directory, "face_detection_yunet_2023mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))

    while True:
        # Capture a frame and read the image
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        # If the image has fewer than 3 channels, convert it to 3 channels
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if channels == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Specify the input size
        height, width, _ = image.shape
        face_detector.setInputSize((width, height))

        # Detect faces
        _, faces = face_detector.detect(image)
        faces = faces if faces is not None else []

        # Draw bounding boxes and landmarks for detected faces
        for face in faces:
            # Bounding box
            box = list(map(int, face[:4]))
            color = (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

            # Landmarks (right eye, left eye, nose, right mouth corner, left mouth corner)
            landmarks = list(map(int, face[4 : len(face) - 1]))
            landmarks = np.array_split(landmarks, len(landmarks) / 2)
            for landmark in landmarks:
                radius = 5
                thickness = -1
                cv2.circle(image, landmark, radius, color, thickness, cv2.LINE_AA)

            # Confidence level
            confidence = face[-1]
            confidence = "{:.2f}".format(confidence)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.5
            thickness = 2
            cv2.putText(
                image, confidence, position, font, scale, color, thickness, cv2.LINE_AA
            )

        # Display the image
        cv2.imshow("face detection", image)
        key = cv2.waitKey(10)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
