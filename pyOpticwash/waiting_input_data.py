import typing

from config import COMMAND_RECEIVING_TIMOUT_S
from pyOpticwash.messages.message import PacketType
from pyOpticwash.messages.message_input import MessageInput


class WaitingInputData:
    def __init__(self, filter_function: typing.Callable[["MessageInput"], bool] = lambda x: True, timeout: float = COMMAND_RECEIVING_TIMOUT_S):
        self.filter_function = filter_function
        self.data = None
        self._timeout = timeout
        self._result: MessageInput | None = None

    @staticmethod
    def waiting_ack(timeout: float = COMMAND_RECEIVING_TIMOUT_S):
        return WaitingInputData(lambda message: message.packet_type == PacketType.ACK, timeout)

    @property
    def timeout(self) -> float:
        return self._timeout

    def try_set_result(self, result: MessageInput):
        if self.filter_function(result):
            self._result = result
            return True

    def get_result(self) -> MessageInput | None:
        return self._result

    def __repr__(self):
        return f"WaitingInputData(filter_function={self.filter_function.__name__}, timeout={self.timeout})"
