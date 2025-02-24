import logging

from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()
    opticwash.state.set_state(OpticwashState.TransactionWaitingRealCard)
    # opticwash.send_keep_transaction_alive()
    opticwash.approve_transaction()
    input("Press enter to stop listening\n")
    opticwash.state.set_state(OpticwashState.Unknown)

    # opticwash.open_cabinet()
    opticwash.stop()
