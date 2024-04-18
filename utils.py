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
                data =  f"Alert! Motion detected at {dt_string}.\nPlease avoid any sudden movements and await further instructions."
                
                self.hook.send(data)
            case "intruder":
                data = f"Warning! Intruder detected at {dt_string}.\nAn alert has been issued. Please remain calm and secure your immediate surroundings."
                human_detection_image = File("/home/derecklhw/Documents/alarmbuzz_autonomous_burglar_detection_robot/output.avi")

                self.hook.send(data, file=human_detection_image)
            case "owner":
                data = f"Notification: Owner recognized at {dt_string}.\nWelcome back! Please proceed with normal activities."
                
                self.hook.send(data)
            case "false_alarm":
                data = f"Notification: False alarm detected at {dt_string}.\nPlease be cautious and report any suspicious activities."
                
                self.hook.send(data)
            case _:
                data = f"Notice: An unidentified event was detected at {dt_string}.\nPlease check your surroundings and report any unusual activities."
                
                self.hook.send(data)
      

