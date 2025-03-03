import logging

from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()

    input("Enter to approve the transaction\n")

    if opticwash.state == OpticwashState.TransactionWaitingApproval:
        opticwash.approve_transaction()
        print("Approving the transaction..")

    else:
        print("Transaction is not waiting for approval")


    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.stop()
