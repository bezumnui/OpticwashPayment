import dataclasses

from pyOpticwash.messages.message import Message, CommandCode, PacketType


class MessageInput(Message):
    def __init__(self, command: CommandCode, packet_type: PacketType, packet_label: int = 0, data: bytes = None,
                 address: int = 0, response_type: int = 0):
        super().__init__(command, packet_type, packet_label, data, address)
        self.response_type = response_type


    @staticmethod
    def unpack(buffer: bytearray):
        address = int.from_bytes(buffer[1:3], 'big')
        packet_label = int.from_bytes(buffer[3:5], 'big')
        raw_command = buffer[5]
        packet_type = PacketType(buffer[6])
        response_type = buffer[7]
        if buffer[8] != 0x32 or buffer[9] != 0x00:
            raise ValueError("Invalid packet header")

        data = buffer[10:58]
        checksum = MessageInput.calculate_checksum(buffer[:59])
        if checksum != buffer[60]:
            raise ValueError("Checksum mismatch")

        raw_command = MessageInput(CommandCode(raw_command), packet_type, packet_label, data, address, response_type)
        raw_command.response_type = response_type
        return raw_command