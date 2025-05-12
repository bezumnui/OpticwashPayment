import logging
import time

import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.misc.utils import get_mdb_by_vendor

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ac_port = get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID)
    mdb_port = get_mdb_by_vendor(config.TERMINAL_VENDOR_ID)
    # while (not ac_port) or (not mdb_port):
    while not (ac_port and mdb_port):
        logging.info("Failed to find the ports. Trying again in 10 seconds")
        time.sleep(10)
        if not ac_port:
            ac_port = get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID)
            continue
        if not mdb_port:
            mdb_port = get_mdb_by_vendor(config.TERMINAL_VENDOR_ID)
            continue

    logging.info("Ports found")
    logging.info("AC Module port: %s", ac_port)
    logging.info("Terminal port: %s", mdb_port)
    opticwash = PyOpticwash()
    logging.info("Initiated")
    opticwash.start()

    while True:
        pass

    opticwash.stop()
