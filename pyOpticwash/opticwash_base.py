import abc

import serial

from pyOpticwash.finite_state_machine import FSMState
from pyOpticwash.handlers.request_payment import RawMDBListener
from pyOpticwash.waiting_input_data import WaitingInputData
from pyOpticwash.messages.message_input import MessageInput
from pyOpticwash.messages.message_output import MessageOutput


class OpticwashBase:

    @abc.abstractmethod
    def send_raw_command(self, data: bytearray):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_command(self, message: MessageOutput):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_command_with_answer(self, waiting_input: WaitingInputData, message: MessageOutput) -> MessageInput | None:
        raise NotImplementedError()

    @property
    def state(self) -> FSMState:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_serial(self) -> serial.Serial:
        raise NotImplementedError()

    @abc.abstractmethod
    def keep_alive(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_raw_mdb(self) -> "RawMDBListener":
        raise NotImplementedError()