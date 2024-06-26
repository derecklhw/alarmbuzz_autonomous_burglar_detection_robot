import serial
import time
import os

from algorithms.yunet import Yunet
from algorithms.generateFeatureDictionary import main as generateFeatureDictionary
from utils import Utils


class App:
    def __init__(self):
        self.username = ""
        self.duration = 0
        self.start_time = 0
        self.camera_id = 0
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.getUserInput()
        self.startSerialConnection()
        self.utils = Utils()

    def getUserInput(self):
        print("╔══════════════════════════════════════╗")
        print("║         Welcome to AlarmBuzz!        ║")
        print("╚══════════════════════════════════════╝")

        # Get the user's name
        self.username = input("What's your name?")

        self.updateOwnerList()
        while True:
            # Check for the specific file presence after updating the owner list
            file_check = "face001.jpg"  # Define the file to check
            directory = os.getcwd() + "/algorithms/"  # Get the current working directory
            
            if file_check in os.listdir(directory):
                break
            else:
                print("\nPlease re-update the owner list as it is invalid.")
                self.updateOwnerList()

        # Greet the user
        print(f"\nHi {self.username}! Let's set up AlarmBuzz duration.\n")

        # Get the user's desired duration
        self.getUserDuration()

    def getUserDuration(self):
        # Define the duration of the loop in seconds
        while True:
            try:
                self.duration = int(
                    input(
                        "How long do you want the alarm buzz to run for? (in seconds) "
                    )
                )
                if self.duration <= 0:
                    print("Sorry, AlarmBuzz duration must be greater than 0.\n")
                elif 0 < self.duration < 60:
                    print("Sorry, AlarmBuzz requires at least 60 seconds to operate.\n")
                else:
                    break
            except ValueError:
                print("Sorry, AlarmBuzz only accept integer :(\n")

        # Confirm the alarm time and duration
        print(f"\nAlarmBuzz will run for {self.duration} seconds. Stay safe!\n")

    def updateOwnerList(self):
        while True:
            update = input("\nWould you like to update the owner list? (y/n) ").lower()
            if update == 'yes' or update == 'y' or update == '':
                generateFeatureDictionary()
                print("Owner list updated successfully.")
                break
            elif update == 'no' or update == 'n':
                print("No updates made to the owner list.")
                break
            else:
                print("Invalid input. No updates made to the owner list.")
                
    def startSerialConnection(self):
        # Open a serial connection and write the 'start' command to the microcontroller
        self.ser.flush()
        time.sleep(2)
        self.ser.write(b"start\n")

        # Get the current time
        self.start_time = time.time()

    def closeSerialConnection(self):
        # Close the serial connection and write the 'stop' command to the microcontroller
        self.ser.write(b"stop\n")
        self.ser.close()
        print(
            f"Thanks for using AlarmBuzz! Sweet dreams and have a great day ahead {self.username}!"
        )

    def run(self):
        try:
            # Loop the script for the specified duration
            while (time.time() - self.start_time) < self.duration:
                # Check if there is any data in the serial buffer
                if self.ser.in_waiting > 0:
                    # Read a line from the serial port
                    line = self.ser.readline().decode().rstrip()
                    if line == "motion":
                        print("Motion detected! Watch out for any suspicious activities.\n")
                        self.utils.sendDiscordNotification("motion")
                        
                        # Initialize a HumanDetector object and check if humans are detected
                        detector = Yunet(self.camera_id)
                        isHuman, isOwner, image = detector.detect_humans()

                        if image is not None:
                            self.utils.saveImage(image)
                        
                        if isHuman and not isOwner:
                            self.utils.sendDiscordNotification("intruder")
                            print("Intruder detected! Initiating alert protocol.\n")
                            # Write 'intruder' to the serial port and print a message
                            self.ser.write(b"intruder\n")

                        elif isHuman and isOwner:
                            self.utils.sendDiscordNotification("owner")
                            print("Owner identified. Disabling security alerts.\n")
                            # Write 'intruder' to the serial port and print a message
                            self.ser.write(b"owner\n")

                        else:
                            self.utils.sendDiscordNotification("false_alarm")
                            print("No intruders detected. Please review the video footage for verification.\n")

        except KeyboardInterrupt:
            print("\nAlarmBuzz has been stopped.")


if __name__ == "__main__":
    app = App()
    app.run()
    app.closeSerialConnection()
