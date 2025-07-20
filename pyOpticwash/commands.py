from abc import ABC

from pyOpticwash.firmware_type import FirmwareType
from pyOpticwash.waiting_input_data import WaitingInputData
from pyOpticwash.messages.message import CommandCode, PacketType
from pyOpticwash.messages.message_input import MessageInput
from pyOpticwash.messages.message_output import MessageOutput
from pyOpticwash.opticwash_base import OpticwashBase


class OpticwashCommands(OpticwashBase, ABC):

    def send_keep_transaction_alive(self):
        self.send_command(MessageOutput(CommandCode.Command, PacketType.ACK, 0, b"\x00"))

    def approve_transaction(self):
        self.send_command(MessageOutput(CommandCode.Command, PacketType.ACK, 0, b"\x01"))

    def decline_transaction(self):
        self.send_command(MessageOutput(CommandCode.Command, PacketType.ACK, 0, b"\x02"))

    def report_server_fault_transaction(self):
        self.send_command(MessageOutput(CommandCode.Command, PacketType.ACK, 0, b"\x03"))

    def cancel_transaction(self):
        self.send_command(MessageOutput(CommandCode.Command, PacketType.ACK, 0, b"\x04"))

    def request_status(self):
        self.send_command(MessageOutput(CommandCode.RequestStatus, PacketType.Send, 0))

    def request_firmware_update(self, firmware_type: FirmwareType):
        self.send_command(MessageOutput(CommandCode.FIRMWARE_UPDATE, PacketType.Send, 0, address=FirmwareType.get_address(firmware_type)))

    def is_in_bootloader_mode(self, firmware_type: FirmwareType):
        return self.send_command_with_answer(WaitingInputData.waiting_ack(), MessageOutput(CommandCode.FIRMWARE_UPDATE, PacketType.Send, 0, address=FirmwareType.get_address(firmware_type))) is not None

    def request_erase_app(self, firmware_type: FirmwareType):
        return self.send_command_with_answer(WaitingInputData.waiting_ack(), MessageOutput(CommandCode.ERASE_APP, PacketType.Send, 0, address=FirmwareType.get_address(firmware_type)))

    def send_block(self, label: int | bytes, firmware_type: FirmwareType, data: bytes) -> MessageInput:
        return self.send_command_with_answer(WaitingInputData.waiting_ack(), MessageOutput(CommandCode.SEND_BLOCK, PacketType.Send, label, data, FirmwareType.get_address(firmware_type)))

    def send_end_blocks(self, firmware_type: FirmwareType) -> MessageInput:
        return self.send_command_with_answer(WaitingInputData.waiting_ack(), MessageOutput(CommandCode.SEND_BLOCK, PacketType.Send, 0, address=FirmwareType.get_address(firmware_type)))

    def request_checksum(self, firmware_type: FirmwareType) -> MessageInput:
        return self.send_command_with_answer(WaitingInputData.waiting_ack(), MessageOutput(CommandCode.CHECKSUM_REQUEST, PacketType.Send, 0, address=FirmwareType.get_address(firmware_type)))

