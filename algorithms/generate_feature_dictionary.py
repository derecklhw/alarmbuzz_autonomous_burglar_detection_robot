import os
import argparse
import numpy as np
import cv2


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser("generate aligned face images from an image")
    parser.add_argument("image", help="input image file path (./image.jpg)")
    args = parser.parse_args()

    # Retrieve the image file path from the arguments
    path = args.image
    directory = os.path.dirname(args.image)
    if not directory:
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, args.image)

    # Clean up directory before processing
    for filename in os.listdir(directory):
        if filename.startswith("face") and (filename.endswith(".jpg") or filename.endswith(".npy")):
            os.remove(os.path.join(directory, filename))

    # Open the image
    image = cv2.imread(path)
    if image is None:
        exit()

    # Convert the image to 3 channels if it is not already
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Load the models
    weights = os.path.join(directory, "face_detection_yunet_2023mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    weights = os.path.join(directory, "face_recognition_sface_2021dec.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    # Specify the input size
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))

    # Detect faces
    _, faces = face_detector.detect(image)

    # Crop the detected faces
    aligned_faces = []
    if faces is not None:
        for face in faces:
            aligned_face = face_recognizer.alignCrop(image, face)
            aligned_faces.append(aligned_face)

    # Display and save the images
    aligned_faces_images = []
    for i, aligned_face in enumerate(aligned_faces):
        cv2.imshow("aligned_face {:03}".format(i + 1), aligned_face)
        image_name = "face{:03}.jpg".format(i + 1)
        aligned_faces_images.append(image_name)
        cv2.imwrite(
            os.path.join(directory, image_name), aligned_face
        )

    for image_path in aligned_faces_images:
        # Retrieve the image file path from the arguments
        path = image_path
        directory = os.path.dirname(image_path)
        if not directory:
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, image_path)

        # Open the image
        image = cv2.imread(path)
        if image is None:
            exit()

        # Convert the image to 3 channels if it is not already
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if channels == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Extract features
        face_feature = face_recognizer.feature(image)

        # Save the features
        basename = os.path.splitext(os.path.basename(image_path))[0]
        dictionary = os.path.join(directory, basename)
        np.save(dictionary, face_feature)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
