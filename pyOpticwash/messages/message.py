import typing
from enum import Enum, auto


class CommandCode(Enum):
    # Control to Pi + Echo
    Status = 0x01
    Command = 0x02
    #  Pi to Control
    RequestStatus = 0x03
    ClearError = 0x04
    UpdatePrice = 0x05
    OpenCabinet = 0x06

    FIRMWARE_UPDATE = 160
    ERASE_APP = 161
    SEND_BLOCK = 162
    BLOCKS_END = 163

    CHECKSUM_REQUEST = 166

class PacketType(Enum):
    Send = 0
    ACK = auto()
    INVALID_COMMAND_RESEND = auto()
    INVALID_PACKET_RESEND = auto()



class Message:
    def __init__(self, command: CommandCode, packet_type: PacketType, packet_label: bytes | int = None, data: bytes = None, address: int = None):
        self.command: CommandCode = command
        self.packet_type: PacketType = packet_type if packet_type else PacketType.Send
        self.address: typing.Optional[int] = address
        self.packet_label: typing.Optional[bytes] = packet_label
        self.data: typing.Optional[bytes] = data

    @staticmethod
    def calculate_checksum(buffer: bytearray):
        checksum = 0
        for byte in buffer:
            checksum += byte
        return checksum & 0xFF

    @staticmethod
    def int_to_bytes(value: int, length: int) -> bytes:
        return value.to_bytes(length, 'big')

    def __repr__(self):
        return f"Message(command={self.command}, packet_type={self.packet_type}, packet_label={self.packet_label}, data={self.data}, address={self.address})"