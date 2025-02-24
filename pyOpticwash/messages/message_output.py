import dataclasses

from pyOpticwash.messages.message import Message

class MessageOutput(Message):
    def pack(self) -> bytearray:
        buffer = bytearray(0)
        buffer.append(0x02)
        if self.address is not None:
            buffer.extend(self.int_to_bytes(self.address, 2))
        else:
            buffer.extend(b'\x00\x00')

        if self.packet_label is not None:
            buffer.extend(self.int_to_bytes(self.packet_label, 2))
        else:
            buffer.extend(b'\x00\x00')

        buffer.append(self.command.value & 0xFF)
        buffer.append(self.packet_type.value & 0xFF)
        buffer.extend(b'\x32\x00')
        if self.data:
            self.data + b"\x00" * (50 - len(self.data))
        buffer.extend(self.data or b'\x00' * 50)
        buffer.append(self.calculate_checksum(buffer[:59]))
        buffer.append(0x03)

        return buffer