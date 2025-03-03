"""
I've implement this logic because opticwash does not provide us the machine sources. After the user
chose the wash mode he will be prompted to swipe the card. And till the card is not swiped the machine won't accept any
signal from the RPI. This is because the display module is responsible for the card swipe. Silly, right? right.
My implementation is simple, I'm speaking to the small rp2040 controller which emulate the swipe signal.
"""
from datetime import time

from gpiozero import OutputDevice
from config import GPIO_HID_TERMINAL_PIN


def send_to_rp2040_swipe():
    display_controller_hid = OutputDevice(GPIO_HID_TERMINAL_PIN)
    display_controller_hid.on()
    time.sleep(.1)
    display_controller_hid.off()