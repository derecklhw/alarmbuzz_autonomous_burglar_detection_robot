import serial
import time

from algorithms.haarcascade import HumanDetector
from utils import Utils

class App:
    username = ""
    duration = 0
    start_time = 0
    camera_id = 0
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    def __init__(self):
        self.getUserInput()
        self.startSerialConnection()

    def getUserInput(self):
        print("╔══════════════════════════════════════╗")
        print("║         Welcome to AlarmBuzz!        ║")
        print("╚══════════════════════════════════════╝")

        # Get the user's name
        self.username = input("What's your name? ")

        # Greet the user
        print(f"\nHi {self.username}! Let's set up AlarmBuzz duration.\n")

        # Define the duration of the loop in seconds
        while True:
            try:
                self.duration = int(input("How long do you want the alarm buzz to run for? (in seconds) "))
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
    
    def startSerialConnection(self):
        # Open a serial connection and write the 'start' command to the microcontroller
        self.ser.flush()
        time.sleep(2)
        self.ser.write(b'start\n')
        
        # Get the current time
        self.start_time = time.time()

    def closeSerialConnection(self):
        # Close the serial connection and write the 'stop' command to the microcontroller
        self.ser.write(b'stop\n')
        self.ser.close()
        print(f"Thanks for using AlarmBuzz! Sweet dreams and have a great day ahead {self.username}!")


    def run(self):
        try:
            # Loop the script for the specified duration
            while (time.time() - self.start_time) < self.duration:
                # Check if there is any data in the serial buffer
                if self.ser.in_waiting > 0:
                    # Read a line from the serial port
                    line = self.ser.readline().decode().rstrip()
                    if line == "motion":
                        # Initialize a HumanDetector object and check if humans are detected
                        detector = HumanDetector(self.camera_id)
                        detection, image = detector.detect_humans()
                        if (detection):
                            # Save the image and send a Discord notification
                            utils = Utils()
                            utils.saveImage(image)     
                            utils.sendDiscordNotification()

                            # Write 'human' to the serial port and print a message
                            self.ser.write(b'human\n')
                            print("AlarmBuzz has detected a human presence! Please check your surroundings.\n")

        except KeyboardInterrupt:
            print("\nAlarmBuzz has been stopped.")

if __name__ == "__main__":
    app = App()
    app.run()
    app.closeSerialConnection()
