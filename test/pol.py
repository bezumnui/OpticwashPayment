import logging
import time

from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    # opticwash.raw_mdb.start_polling()
    opticwash.raw_mdb.mdb.send_raw(b"R,10")
    opticwash.raw_mdb.mdb.send_raw(b"R,11,0003000000")
    opticwash.raw_mdb.mdb.send_raw(b"R,14,01")
    while True:
        opticwash.raw_mdb.mdb.send_raw(b"R,12")
        time.sleep(0.1)
        # opticwash.raw_mdb.mdb.send_raw(input().encode())
        # input("Press enter...")
