import cv2
import os
from datetime import datetime
from dotenv import load_dotenv
from dhooks import Webhook, File

load_dotenv()

class Utils:
    save_image_path = os.getenv('SAVE_IMAGE_PATH')
    human_detection_image_path = ""
    hook = Webhook(os.getenv('DISCORD_WEBHOOK_URL'))

    def saveImage(self, image):
        # Format the current time as a string
        current_time_image_format = self.current_time.strftime("%Y%m%d_%H%M%S")

        # Save the image to the specified path
        self.human_detection_image_path = f"{self.save_image_path}{current_time_image_format}.jpg"
        cv2.imwrite(self.human_detection_image_path, image)

    def sendDiscordNotification(self, action):
        # Format the current time as a string
        self.current_time = datetime.now()
        dt_string = self.current_time.strftime("%d/%m/%Y %H:%M:%S")
        
        match action:
            case "motion":
                data =  f"Alert: Motion detected at {dt_string}."
                
            case "intruder":
                data = f"Warning: Intruder detected at {dt_string}."
             
            case "owner":
                data = f"Notification: Owner recognized at {dt_string}."
                
            case "false_alarm":
                data = f"Notification: No intruder detected at {dt_string}."
                
            case _:
                data = f"Notice: An unidentified event was detected at {dt_string}."

        if action != "motion":
            human_detection_image = File("./output.avi")
            self.hook.send(data, file=human_detection_image)
        else:
            self.hook.send(data)
      

