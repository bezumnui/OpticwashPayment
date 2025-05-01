import logging

from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    # opticwash.raw_mdb.start_polling()
    while True:
        opticwash.raw_mdb.mdb.send_raw(input().encode())
        input("Press enter...")
