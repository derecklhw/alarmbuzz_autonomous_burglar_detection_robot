import cv2
import os
from datetime import datetime
from dotenv import load_dotenv
from dhooks import Webhook, File, Embed

load_dotenv()

class Utils:
    save_image_path = os.getenv('SAVE_IMAGE_PATH')
    intrusion_image_path = ""
    hook = Webhook(os.getenv('DISCORD_WEBHOOK_URL'))
    video_motion_path = "./output.avi"

    def saveImage(self, image):
        self.current_time = datetime.now()
        # Format the current time as a string
        current_time_image_format = self.current_time.strftime("%Y%m%d_%H%M%S")

        # Save the image to the specified path
        self.intrusion_image_path = f"{self.save_image_path}{current_time_image_format}.jpg"
        cv2.imwrite(self.intrusion_image_path, image)

    def sendDiscordNotification(self, action):       
        match action:
            case "motion":
                data =  f"Alert: Motion detected."
                embed_color = 0XFFD700
            case "intruder":
                data = f"Warning: Intruder detected."
                embed_color = 0XFF0000
            case "owner":
                data = f"Notification: Owner recognized."
                embed_color = 0X008000
                
            case "false_alarm":
                data = f"Notification: No intruder detected. Please review the video footage for verification."
                embed_color = 0X0000FF
            case _:
                data = f"Error: An unidentified event was detected."
                embed_color = 0XFFA500

        embed = Embed(
            description=data,
            color=embed_color,
            timestamp='now'
        )

        if action != "motion":
            self.hook.send(embed=embed)
            if action == "owner" or action == "intruder":
                self.hook.send(file=File(self.intrusion_image_path))

            self.hook.send(file=File(self.video_motion_path))
        else:
            self.hook.send(embed=embed)
      

