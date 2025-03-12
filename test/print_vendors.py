from serial.tools import list_ports

if __name__ == '__main__':
    device_list = list_ports.comports()
    for device in device_list:
        print(device.device, hex(device.vid) if device.vid else "None")
    print("Done")