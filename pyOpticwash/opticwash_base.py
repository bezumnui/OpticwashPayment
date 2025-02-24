import abc

import serial

from pyOpticwash.finite_state_machine import FSMState
from pyOpticwash.messages.message_output import MessageOutput
from pyOpticwash.pyMDBTerminal.mdb_client import MDBClient


class OpticwashBase:

    @abc.abstractmethod
    def send_raw_command(self, data: bytearray):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_command(self, message: MessageOutput):
        raise NotImplementedError()

    @property
    def state(self) -> FSMState:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_serial(self) -> serial.Serial:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_mdb_client(self) -> "MDBClient":
        raise NotImplementedError()

    @abc.abstractmethod
    def keep_alive(self):
        raise NotImplementedError()

