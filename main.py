import serial
import time

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    time.sleep(2)

    ser.write(b'start\n')

    # Define the duration of the loop in seconds
    duration = 60

    # Get the current time
    start_time = time.time()

    # Loop the script for the specified duration
    while (time.time() - start_time) < duration:
        print("running")
    
    ser.write(b'stop\n')
    ser.close()