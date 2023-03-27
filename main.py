import serial
import time

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    time.sleep(2)

    ser.write(b'start\n')
    time.sleep(30)    
    ser.write(b'stop\n')
    ser.close()