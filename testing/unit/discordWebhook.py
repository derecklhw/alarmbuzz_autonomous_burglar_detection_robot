from dhooks import Webhook, File
from datetime import datetime

hook = Webhook("https://discord.com/api/webhooks/1090684363714351144/NMGFwquH-LvDjJBHL8SmxQtKRjFjT8ZQ6Nqb-r8IMZP7fkqLJHylMijY1J8FRv4zH3Us")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

data = f"Attention! Our sensors have detected the presence of a human being as of {dt_string}.\nFor safety reasons, please stand still and wait for further instructions."
human_detection_image = File("../burglar.jpg")

hook.send(data, file=human_detection_image)