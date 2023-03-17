import cv2
from keras.models import load_model

from humanDetection import HumanDetection

def triggerHumanDetection():
    # Start capturing the camera feed
    cap = cv2.VideoCapture(0)
    # Load the trained model
    model = load_model(r"Models/human.h5")

    while True:
        ret, frame = cap.read()

        # Initialize the class
        human = HumanDetection(frame, model)

        # Process the frame
        processed_frame, processed_label = human.process_frame()

        # Display the frame
        cv2.imshow("Human Detection", processed_frame)

        if processed_label == "HUMAN":
            return "human detection"

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    triggerHumanDetection()
