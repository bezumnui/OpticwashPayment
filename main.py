import os
import sys
import logging
import time

import config
from logger import setup_logger
from pyOpticwash.client import PyOpticwash
from pyOpticwash.misc.utils import get_mdb_by_vendor
from timeout_watchdog import TimeoutWatchdog

SECONDS_TO_CONNECT_MDB = 30

def restart_application():
    os.execv(sys.argv[0], sys.argv)

def start_mdb_using_watchdog(opticwash: PyOpticwash):
    watchdog = TimeoutWatchdog(restart_application, SECONDS_TO_CONNECT_MDB)
    watchdog.start()
    opticwash.start_mdb()
    opticwash.reset_mdb()
    opticwash.stop_mdb()
    time.sleep(5)
    opticwash.start_mdb()
    opticwash.start_polling()
    watchdog.stop()

def wait_for_devices_initialization():
    ac_port = get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID)
    mdb_port = get_mdb_by_vendor(config.TERMINAL_VENDOR_ID)

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


def poll_application(ac_port, opticwash):
    while True:
        try:
            opticwash.start_machine(ac_port)
        except Exception as e:
            logging.exception(e)
            continue


def main():
    setup_logger()
    wait_for_devices_initialization()
    opticwash = PyOpticwash()
    logging.info("Initiated")
    start_mdb_using_watchdog(opticwash)
    poll_application(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID), opticwash)
    opticwash.stop()


if __name__ == '__main__':
    main()
