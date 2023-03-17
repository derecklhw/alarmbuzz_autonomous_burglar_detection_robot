import cv2
import numpy as np
from keras.models import load_model


class HumanDetection:
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        self.humanlist = ["NOT-HUMAN", "HUMAN"]

    def process_frame(self):
        # Preprocess the frame
        resized = cv2.resize(self.frame, (86, 48))
        image_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # Use the model to predict whether there is fire in the frame
        prediction = self.model.predict(np.expand_dims(image_rgb, axis=0))

        print(
            f"Prediction is: {prediction} and the label is: {[np.argmax(prediction)]}"
        )
        label = self.humanlist[np.argmax(prediction)]

        cv2.putText(self.frame, label, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return self.frame, label


if __name__ == "__main__":
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

        # if processed_label == "HUMAN":
        #     return "human detection"

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
