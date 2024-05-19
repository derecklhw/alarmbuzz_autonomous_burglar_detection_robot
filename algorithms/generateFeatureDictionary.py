import os
import argparse
import numpy as np
import cv2


def main():
    while True:
        # Ask the user if they want to upload an image or capture a new one
        choice = input("\nDo you want to upload or capture an image? (u/c): ").lower()
        if choice == "upload" or choice == "u":
            # Ask the user for the image file path
            path = input("\nPlease enter the path to the image file (e.g., ./image.jpg): ")
            directory = os.path.dirname(path)
            if not directory:
                directory = os.path.dirname(__file__)
            path = os.path.join(directory, path)

            # Check if the image exists
            if not os.path.exists(path):
                print(f"No file found at {path}.\n")
                retry = input("Would you like to retry or cancel? (r/c): ").lower()
                if retry == "cancel" or retry == "c":
                    print("Operation canceled by the user.")
                    return
                elif retry == "retry" or retry == "r":
                    continue
                else:
                    print("Invalid input, please enter 'retry' or 'cancel'.")
                    continue
            else:
                print("Image successfully loaded.")
                break
        elif choice == "capture" or choice == "c":
            print("Please capture the image using your device's camera.")
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Open the default camera
            if not cap.isOpened():
                print("Error: Camera could not be opened.")
                break

            while True:
                ret, src = cap.read()  # Read a frame from the video stream
                frame = cv2.flip(src, 0)
                if not ret:
                    print("Failed to capture image from camera.")
                    break
                cv2.imshow('Press q to capture image', frame)  # Display the frame

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Wait for a key press for 1 ms
                     # save the image to disk
                    path = 'algorithms/capture.png'
                    directory = os.path.dirname(path)
                    cv2.imwrite(path, frame)
                    print("Image captured and saved successfully.")
                    break
            
            cv2.destroyAllWindows()  # Destroy all the created windows
            cap.release()  # Release the camera
            break
            
        else:
            print("Invalid choice. Please type 'upload' or 'capture'.")

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
