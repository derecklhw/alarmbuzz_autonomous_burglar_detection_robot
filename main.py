import serial
import time
import sys
import os
import cv2

import hogDescriptor

if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║         Welcome to AlarmBuzz!        ║")
    print("╚══════════════════════════════════════╝")

    # Wait for 1 second before continuing
    time.sleep(1)

    # Get the user's name
    name = input("What's your name? ")

    # Greet the user
    print(f"\nHi {name}! Let's set up AlarmBuzz duration.\n")

    # Wait for 1 second before continuing
    time.sleep(1)

    # Define the duration of the loop in seconds
    while True:
        try:
            duration = int(input("How long do you want the alarm buzz to run for? (in seconds) "))
            if duration <= 0:
                print("Sorry, AlarmBuzz only accept integer greater than 0\n")
            else:
                break
        except ValueError:
            print("Sorry, AlarmBuzz only accept integer :(\n")
            
    # Confirm the alarm time and duration
    print(f"\nAlarmBuzz will run for {duration} seconds. Stay safe!\n")

    # Open a serial connection and write the 'start' command to the microcontroller
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    time.sleep(2)
    ser.write(b'start\n')

    # Get the current time
    start_time = time.time()

    try:
        # Loop the script for the specified duration
        while (time.time() - start_time) < duration:
            # Check if there is any data in the serial buffer
            if ser.in_waiting > 0:
                # Read a line from the serial port
                line = ser.readline().decode().rstrip()
                if line == "motion":
                    # Initialize a HumanDetector object and check if humans are detected
                    detector = hogDescriptor.HumanDetector(0)
                    if (detector.detect_humans()):
                        # If humans are detected, write 'human' to the serial port and print a message
                        ser.write(b'human')

    except KeyboardInterrupt:
        print("AlarmBuzz has been stopped.")

    print("Thanks for using AlarmBuzz! Sweet dreams and have a great day ahead!")
    
    # Close the serial connection and write the 'stop' command to the microcontroller
    ser.write(b'stop\n')
    ser.close()
