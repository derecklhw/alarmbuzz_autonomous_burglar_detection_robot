import cv2
import imutils
import time
from datetime import datetime
from dhooks import Webhook, File

class HumanDetector:
    def __init__(self, camera_id):
        # Initialize the HOG descriptor with the default people detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Initialize the video capture device
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

        # Set the duration of the human detection loop in seconds
        self.duration = 20
        
    def detect_humans(self):
        # Get the current time in seconds
        start_time = time.time()

        # Loop until the duration of the human detection loop has elapsed
        while (time.time() - start_time) < self.duration:
            # Read a frame from the video capture device
            ret, src = self.cap.read()

            # Flip the frame vertically to correct the orientation
            image = cv2.flip(src, 0)

            if ret:
                # Resize the frame to a smaller size to speed up the detection
                image = imutils.resize(image, 
                                       width=min(400, image.shape[1]))

                # Detect humans in the frame using the HOG descriptor
                (regions, _) = self.hog.detectMultiScale(image,
                                                          winStride=(4, 4),
                                                          padding=(4, 4),
                                                          scale=1.05)

                # If humans are detected, take a photo and send a notification to Discord
                for (x, y, w, h) in regions:
                    # cv2.rectangle(image, (x, y),
                    #               (x + w, y + h), 
                    #               (0, 0, 255), 2)

                    # Take a photo of the frame when humans are detected
                    current_time = datetime.now()
                    current_time_image_format = current_time.strftime("%Y%m%d_%H%M%S")
                    human_detection_image_path = f"images/photo_{current_time_image_format}.jpg"
                    cv2.imwrite(human_detection_image_path, image)
                        
                    # Release the video capture device and close the image window
                    self.cap.release()
                    cv2.destroyAllWindows()
                    
                    # Send a message and image to Discord using a Webhook object
                    hook = Webhook("https://discord.com/api/webhooks/1090684363714351144/NMGFwquH-LvDjJBHL8SmxQtKRjFjT8ZQ6Nqb-r8IMZP7fkqLJHylMijY1J8FRv4zH3Us")

                    # Format the current time as a string
                    dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")

                    # Create a message with the current time and instructions for the user
                    data = f"Attention! Our sensors have detected the presence of a human being as of {dt_string}.\nFor safety reasons, please stand still and wait for further instructions."
                    human_detection_image = File(human_detection_image_path)
                    
                    # Send the message and image to the Discord webhook
                    hook.send(data, file=human_detection_image)

                    print("AlarmBuzz has detected a human presence! Please check your surroundings.\n")
                    return True

                # Display the image with bounding boxes around detected humans
                cv2.imshow("Image", image)

                # Wait for a key press and exit the loop if the 'q' key is pressed
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release the video capture device and close the image window when done
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create a HumanDetector object with the default camera ID (0)
    detector = HumanDetector(0)

    # Call the detect_humans method to start detecting humans
    detector.detect_humans()
