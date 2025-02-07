import dataclasses
import typing


@dataclasses.dataclass
class Command:
    command: int
    packet_type: int
    address: typing.Optional[int]
    packet_label: typing.Optional[int]
    data: typing.Optional[bytes]

    def raw_command(self):
        buffer = bytearray(0)
        buffer.append(0x02)
        if self.address is not None:
            buffer.extend(Command.int_to_bytes(self.address, 2))
        else:
            buffer.extend(b'\x00\x00')

        if self.packet_label is not None:
            buffer.extend(Command.int_to_bytes(self.packet_label, 2))
        else:
            buffer.extend(b'\x00\x00')

        buffer.append(self.command & 0xFF)
        buffer.append(self.packet_type & 0xFF)
        buffer.extend(b'\x32\x00')
        buffer.extend(self.data or b'\x00' * 50)
        buffer.append(Command.calculate_checksum(buffer[:59]))
        buffer.append(0x03)

        return buffer

    @staticmethod
    def from_raw(buffer: bytearray):
        address = int.from_bytes(buffer[1:3], 'big')
        packet_label = int.from_bytes(buffer[3:5], 'big')
        command = buffer[5]
        packet_type = buffer[6]
        data = buffer[8:58]

        checksum = Command.calculate_checksum(buffer[:59])
        print(f"Checksum: {hex(checksum)}, Waiting for {hex(buffer[59])}")
        if checksum != buffer[59]:
            raise ValueError("Checksum mismatch")

        command = Command(command, packet_type, address, packet_label, data)
        return command



    @staticmethod
    def calculate_checksum(buffer: bytearray):
        checksum = 0
        for byte in buffer:
            checksum += byte
        print(f"Checksum: {hex(checksum & 0xFF)}")
        return checksum & 0xFF

    @staticmethod
    def int_to_bytes(value: int, length: int) -> bytes:
        return value.to_bytes(length, 'big')