from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState

if __name__ == '__main__':
    opticwash = PyOpticwash()
    opticwash.start()
    opticwash.state.set_state(OpticwashState.TransactionWaitingRealCard)

    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.stop()
