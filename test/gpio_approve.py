import logging
import time
from time import sleep

from gpiozero import OutputDevice

from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState

display_controller_hid = OutputDevice(17)

def send_to_rp2040_swipe():
    display_controller_hid.on()
    time.sleep(.1)
    display_controller_hid.off()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()
    input("Press enter to approve\n")
    opticwash.send_keep_transaction_alive()
    print("Swiping..")
    print("Approving transaction..")
    send_to_rp2040_swipe()
    sleep(2)
    opticwash.approve_transaction()
    print("Transaction approved")
    input("Press enter to stop listening\n")


    # opticwash.open_cabinet()
    opticwash.stop()
