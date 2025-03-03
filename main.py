import logging

from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()

    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.stop()
