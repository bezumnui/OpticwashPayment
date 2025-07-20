import time

import logging

import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.firmware import FirmwareType, Firmware
from pyOpticwash.misc.utils import get_mdb_by_vendor

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    blocks = []
    with open("Display513.X.test.hex", "r") as file:
        for line in file.readlines():
            blocks.append(line.replace("\n", ""))

    # print(blocks, end='\n')
    opticwash = PyOpticwash()

    opticwash.start_machine(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID))
    opticwash.request_firmware_update(FirmwareType.DC_Module)
    # opticwash.stop()
    # time.sleep(20)
    # opticwash.start()
    print(f"is in bootloader: {opticwash.is_in_bootloader_mode(FirmwareType.DC_Module)}")
    firmware = Firmware(opticwash)
    firmware.send_blocks(blocks, FirmwareType.Display_Module)
    # opticwash.send_end_blocks()

