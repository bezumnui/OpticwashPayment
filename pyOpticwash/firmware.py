import logging

from pyOpticwash.firmware_type import FirmwareType
from pyOpticwash.commands import OpticwashCommands



class Firmware:
    def __init__(self, client: OpticwashCommands):
        self.client = client

    @staticmethod
    def string_to_byte_array(hex_str: str) -> bytearray:

        if len(hex_str) % 2:
            raise ValueError(f"Hex string length must be even {len(hex_str)}:" + hex_str)
        return bytearray(int(hex_str[i: i + 2], 16) for i in range(0, len(hex_str), 2))

    def send_blocks(self, blocks: list[str], firmware_type: FirmwareType):
        num = 0
        num2 = 0

        for i in range(len(blocks)):
            text = blocks[i]
            logging.info(f"Flashing {i} / {len(blocks)} block")
            if (num != 0 or not text.startswith("*")) and (num != 1 or not text.startswith("?")):
                payload = bytearray()
                payload.append(0x3A)  # 58
                payload.extend(self.string_to_byte_array(text[1:]))

                input_message = self.client.send_block(num2 & 0xFF, firmware_type, bytes(payload))

                num += 1
                num2 = (num2 + 1) & 0xFF  # wrap after 255

                if input_message is None:
                    logging.error(f"Timeout when sending block {num}")
                    raise TimeoutError(f"Timeout when sending block {num}.")


        input_message = self.client.send_end_blocks(firmware_type)

        if input_message is None:
            logging.error(f"Timeout when sending end of the file {num}")
            raise TimeoutError(f"Timeout when sending end of the file {num}.")