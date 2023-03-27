import serial
import time

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)

    while True:
        ser.write(b'run\n')