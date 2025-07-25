import logging
from time import sleep

from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start_mdb()
    input("Press enter to approve\n")
    opticwash.send_keep_transaction_alive()
    print("Approving transaction..")
    sleep(2)
    opticwash.approve_transaction()
    print("Transaction approved")
    input("Press enter to stop listening\n")


    # opticwash.open_cabinet()
    opticwash.stop()
