import cv2
from keras.models import load_model
import time

from humanDetection import HumanDetection

def triggerHumanDetection():
    # Start capturing the camera feed
    cap = cv2.VideoCapture(0)
    # Load the trained model
    model = load_model(r"Models/human.h5")

    # Set the start time
    start_time = time.time()

    # Set the duration to 10 seconds
    duration = 10

    while (time.time() - start_time) < duration:
        # Code to be executed during the 10 second limit
        ret, frame = cap.read()

        # Initialize the class
        human = HumanDetection(frame, model)

        # Process the frame
        processed_frame, processed_label = human.process_frame()

        # Display the frame
        cv2.imshow("Human Detection", processed_frame)

        if processed_label == "HUMAN":
            return "human detected"

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    return "no human detected"

if __name__ == "__main__":
    humanDetection = triggerHumanDetection()
    print(humanDetection)