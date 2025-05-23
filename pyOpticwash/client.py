import logging
import typing

import serial

from pyOpticwash.handlers.request_payment import RawMDBListener
from pyOpticwash.listener import Listener
from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.finite_state_machine import FSMState, OpticwashState
from pyOpticwash.machine_keepalive import OpticwashScheduler
from py_mdb_terminal.mdb_client import MDBClient
from pyOpticwash.messages.message import CommandCode, PacketType
from pyOpticwash.messages.message_output import MessageOutput
from pyOpticwash.opticwash_base import OpticwashBase


class PyOpticwash(OpticwashCommands, OpticwashBase):





    def __init__(self):
        super().__init__()
        self.packet_id = 0
        self.ser: typing.Optional[serial.Serial] = None
        self._state = FSMState(OpticwashState.Standby)
        self.listener = Listener(self)
        self.mdb_client = MDBClient()
        self.scheduler = OpticwashScheduler(self)
        self.raw_mdb = RawMDBListener(self)

    def start(self, port='/dev/ttyACM0'):
        self.scheduler.start_scheduler()
        logging.debug("PyOpticwash: Starting serial port")
        self.ser = serial.Serial(port, 9600)
        logging.debug("PyOpticwash: Starting the listener")
        self.listener.start()
        logging.debug("PyOpticwash: Starting MDB client, Polling")
        self.raw_mdb.start_polling()


    def stop(self):
        self.listener.stop()
        self.ser.close()
        self.scheduler.stop_scheduler()

    def open_cabinet(self):
        message = MessageOutput(CommandCode.OpenCabinet, PacketType.Send, 0)
        self.send_command(message)

    def send_raw_command(self, data: bytearray):
        logging.debug(f"Sending raw data: {data.hex()}")
        self.ser.write(data)

    def send_command(self, message: MessageOutput):
        logging.info(f"Sending message: {message}")
        message.packet_label = self.packet_id & 0xFFFF
        self.packet_id += 1
        self.send_raw_command(message.pack())

    def get_serial(self) -> serial.Serial:
        return self.ser

    def get_mdb_client(self):
        return self.mdb_client

    @property
    def state(self) -> FSMState:
        return self._state

    def keep_alive(self):
        self.scheduler.keepalive()

    def get_raw_mdb(self):
        return self.raw_mdb



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    opticwash.start()
    opticwash.keep_alive()

    input("Press enter to stop listening\n")

    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.stop()
