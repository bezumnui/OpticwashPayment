import time

import logging
from serial.tools import list_ports

import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.firmware import FirmwareType, Firmware
from pyOpticwash.misc.utils import get_mdb_by_vendor

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    opticwash = PyOpticwash()


    opticwash.start_machine(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID))
    opticwash.request_erase_app(FirmwareType.Display_Module)


