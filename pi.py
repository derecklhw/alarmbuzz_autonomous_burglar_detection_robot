import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

# Initialize the Picamera V2
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Load the trained model
model = load_model(r"Models/human.h5")

# Process the frames
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    image = frame.array

    # Preprocess the frame
    resized = cv2.resize(image, (86, 48))
    image_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    # Use the model to predict whether there is a human in the frame
    prediction = model.predict(np.expand_dims(image_rgb, axis=0))
    label = humanlist[np.argmax(prediction)]

    # Display the frame with label
    cv2.putText(image, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Human Detection", image)

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

