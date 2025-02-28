import time

from gpiozero import OutputDevice

display_controller_hid = OutputDevice(17)

if __name__ == '__main__':
    while True:
        input("Press enter to on\n")
        display_controller_hid.on()
        time.sleep(.2);
        display_controller_hid.off()