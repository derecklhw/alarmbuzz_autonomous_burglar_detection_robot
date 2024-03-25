import cv2
import os
from datetime import datetime
from dotenv import load_dotenv
from dhooks import Webhook, File

load_dotenv()

class Utils:
    current_time = datetime.now()
    save_image_path = os.getenv('SAVE_IMAGE_PATH')
    human_detection_image_path = ""
    hook = Webhook(os.getenv('DISCORD_WEBHOOK_URL'))

    def saveImage(self, image):
        # Format the current time as a string
        current_time_image_format = self.current_time.strftime("%Y%m%d_%H%M%S")

        # Save the image to the specified path
        self.human_detection_image_path = f"{self.save_image_path}{current_time_image_format}.jpg"
        cv2.imwrite(self.human_detection_image_path, image)

    def sendDiscordNotification(self):
        # Format the current time as a string
        dt_string = self.current_time.strftime("%d/%m/%Y %H:%M:%S")

        # Create a message with the current time and instructions for the user
        data = f"Attention! Our sensors have detected the presence of a human being as of {dt_string}.\nFor safety reasons, please stand still and wait for further instructions."
        
        # Send the message and image to the Discord webhook
        human_detection_image = File(self.human_detection_image_path)
        self.hook.send(data, file=human_detection_image)
