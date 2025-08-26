import re

from typing import List, Optional, Tuple

import time

import logging
from serial.tools import list_ports

import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.firmware import FirmwareType, Firmware
from pyOpticwash.misc.utils import get_mdb_by_vendor

def validate_firmware_blocks(
    blocks: List[str],
) -> Tuple[bool, Optional[str], Optional[str]]:
    version_pattern = re.compile(r"^\*\d{4,5}$")
    checksum_pattern = re.compile(r"^\?[0-9A-F]{4}$")
    data_pattern = re.compile(r"^:[a-fA-F\d]*$")

    if not blocks:
        return False, "Blocks is empty", None

    checksum_value: Optional[str] = None

    for index, block_text in enumerate(blocks):
        if len(block_text) > 43:
            return (
                False,
                f"Too many characters in a single line. line: {index + 1}",
                None,
            )

        if index == 0:
            if not version_pattern.fullmatch(block_text):
                return False, "Invalid version info or it's missing", None

        elif index == 1:
            if not checksum_pattern.fullmatch(block_text):
                return False, "Invalid checksum info or it's missing", None
            checksum_value = block_text[1:]

        else:
            if len(block_text) % 2 != 1:
                return False, f"Invalid length. line:{index + 1}", None
            if not data_pattern.fullmatch(block_text):
                return False, f"Invalid data format. line:{index + 1}", None
            if not validate_checksum(string_to_byte_array(block_text[1:])):
                return False, f"Invalid data checksum. line:{index + 1}", None

    return True, None, checksum_value


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    blocks = []
    # with open("test/update.hex", "r") as file:
    with open("update.hex", "r") as file:
        for line in file.readlines():
            # blocks.append(line.replace("\n", ""))
            blocks.append(line.replace("\n", ""))

    print(validate_firmware_blocks(blocks))
    exit()
    # print(blocks, end='\n')
    opticwash = PyOpticwash(False)
    opticwash.start_machine(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID))

    opticwash.request_firmware_update(FirmwareType.DC_Module)
    # opticwash.request_erase_app(FirmwareType.DC_Module)
    # exit()
    # opticwash.stop()
    # time.sleep(3)
    # opticwash.start_machine(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID))
    print(f"is in bootloader: {opticwash.is_in_bootloader_mode(FirmwareType.DC_Module)}")
    firmware = Firmware(opticwash)
    firmware.send_blocks(blocks, FirmwareType.Display_Module)

    opticwash.send_end_blocks(FirmwareType.Display_Module)


def string_to_byte_array(hex_string: str) -> List[int]:
    return [int(hex_string[i : i + 2], 16) for i in range(0, len(hex_string), 2)]


def validate_checksum(data_bytes: List[int]) -> bool:
    return sum(data_bytes) % 256 == 0

