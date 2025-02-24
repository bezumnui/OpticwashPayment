import logging

from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()
    input("Press enter to approve\n")
    opticwash.approve_transaction()
    input("Press enter to stop listening\n")


    # opticwash.open_cabinet()
    opticwash.stop()
