import serial

if __name__ == '__main__':
    ser = serial.Serial("/dev/serial0", 4800, timeout=1)
    ser.write(b"RR\n\r")
    while True:
        line = ser.read()  # до \n или timeout
        if line:
            print(line)
        else:
            print("No data")
        input()
        ser.write(b"RRRR\n\r")

