import time

import logging
import typing

import serial

from pyOpticwash.handlers.request_payment import RawMDBListener
from pyOpticwash.listener import Listener, WaitingInputData
from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.finite_state_machine import FSMState, OpticwashState
from pyOpticwash.machine_keepalive import OpticwashScheduler
from pyOpticwash.messages.message_input import MessageInput
from py_mdb_terminal.mdb_client import MDBClient
from pyOpticwash.messages.message import CommandCode, PacketType
from pyOpticwash.messages.message_output import MessageOutput
from pyOpticwash.opticwash_base import OpticwashBase


class PyOpticwash(OpticwashCommands, OpticwashBase):
    def __init__(self, enable_mdb = True):
        super().__init__()
        self.packet_id = 0
        self.ser: typing.Optional[serial.Serial] = None
        self._state = FSMState(OpticwashState.Standby)
        self.listener = Listener(self)
        self.scheduler = OpticwashScheduler(self)

        if enable_mdb:
            self.raw_mdb = RawMDBListener()

        self.is_work = False
        self.mdb_enabled = enable_mdb

    def start_mdb(self):
        logging.info("PyOpticwash: Starting MDB")
        self.raw_mdb.start()

    def start_telemetry(self):
        logging.info("PyOpticwash: Starting telemetry")
        self.raw_mdb.mdb.send_raw_message(b"X,1")


    def stop_mdb(self):
        logging.info("PyOpticwash: Stopping MDB")
        self.raw_mdb.stop()

    def start_polling(self):
        logging.info("PyOpticwash: Starting MDB Polling")
        self.raw_mdb.start_polling()


    def reset_mdb(self):
        logging.info("PyOpticwash: Resetting MDB client")
        self.raw_mdb.reset()


    def start_machine(self, port='/dev/ttyACM1'):
        self.is_work = True
        self.scheduler.start_scheduler()
        logging.debug("PyOpticwash: Starting serial port")
        self.ser = serial.Serial(port, 9600)
        logging.debug("PyOpticwash: Starting the listener")
        self.listener.start()

    def idle(self):
        while self.is_work:
            time.sleep(0.1)

    def stop(self):
        self.listener.stop()
        self.ser.close()
        self.scheduler.stop_scheduler()
        self.is_work = False


    def open_cabinet(self):
        message = MessageOutput(CommandCode.OpenCabinet, PacketType.Send, 0)
        self.send_command(message)

    def send_raw_command(self, data: bytearray):
        logging.debug(f"Sending raw data: {data.hex()}")
        for byte, i in zip(data, range(len(data))):
            print(f"{i}:{hex(byte)}", end=' ')

        self.ser.write(data)

    def send_command_with_answer(self, waiting_input: WaitingInputData, message: MessageOutput) -> MessageInput | None:
        self.listener.set_input(waiting_input)
        self.send_command(message)
        return self.listener.get_input_blocking(waiting_input)

    def send_command(self, message: MessageOutput):
        logging.info(f"Sending message: {message}")
        message.packet_label = self.packet_id & 0xFFFF
        self.packet_id += 1
        self.send_raw_command(message.pack())

    def get_serial(self) -> serial.Serial:
        return self.ser

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
    opticwash.start_mdb()
    opticwash.keep_alive()
    opticwash.keep_alive()

    input("Press enter to stop listening\n")

    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.stop()
