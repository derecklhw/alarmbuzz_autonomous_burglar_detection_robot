import serial
import time
import sys
import os
import cv2

from humanDetection import hogDescriptor

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    time.sleep(2)

    ser.write(b'start\n')

    # Define the duration of the loop in seconds
    duration = 60

    # Get the current time
    start_time = time.time()

    try:
        # Loop the script for the specified duration
        while (time.time() - start_time) < duration:
            # Check if there is any data in the serial buffer
            if ser.in_waiting > 0:
                # Read a line from the serial port
                line = ser.readline().decode().rstrip()
                print("Received from serial:", line)
                if line == "motion":
                    detector = hogDescriptor.HumanDetector(0)
                    if (detector.detect_humans()):
                        ser.write(b'human')
                        print("human")

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping script...")

    ser.write(b'stop\n')
    ser.close()
