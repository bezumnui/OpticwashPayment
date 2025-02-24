from abc import ABC

from pyOpticwash.messages.message import CommandCode, PacketType
from pyOpticwash.messages.message_output import MessageOutput
from pyOpticwash.opticwash_base import OpticwashBase


class OpticwashCommands(OpticwashBase, ABC):

    def send_keep_transaction_alive(self):
        self.send_command(MessageOutput(CommandCode.Swipe, PacketType.ACK, 0, b"\x00"))

    def approve_transaction(self):
        self.send_command(MessageOutput(CommandCode.Swipe, PacketType.ACK, 0, b"\x01"))

    def decline_transaction(self):
        self.send_command(MessageOutput(CommandCode.Swipe, PacketType.ACK, 0, b"\x02"))

    def report_server_fault_transaction(self):
        self.send_command(MessageOutput(CommandCode.Swipe, PacketType.ACK, 0, b"\x03"))

    def cancel_transaction(self):
        self.send_command(MessageOutput(CommandCode.Swipe, PacketType.ACK, 0, b"\x04"))

    def request_status(self):
        self.send_command(MessageOutput(CommandCode.RequestStatus, PacketType.Send, 0))

