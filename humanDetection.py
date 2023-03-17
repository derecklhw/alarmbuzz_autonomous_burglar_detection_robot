import cv2
import numpy as np
from keras.models import load_model

model = load_model(r"human.h5")

firelist=['Human','Not-Human']
def process_frame(image):
    # Preprocess the frame
    resized = cv2.resize(image, (86, 48))
    image_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    # Use the model to predict whether there is fire in the frame
    prediction = model.predict(np.expand_dims(image_rgb, axis=0))
   

    label = firelist[np.argmax(prediction)]
    print (prediction)

    cv2.putText(image, label, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image


# if __name__ == "__main__":
#     # Start capturing the camera feed
#     cap = cv2.VideoCapture(0)
#     # Load the trained model


while True:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    # Initialize the class
    # img=cv2.imread(r"dereck.jpeg")
    fire = process_frame(frame)
    cv2.imshow("Fire Detection", fire)

        # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
