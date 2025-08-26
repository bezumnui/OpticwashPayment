from datetime import datetime

import typing

import logging
import threading
import time

import serial

from config import COMMAND_RECEIVING_TIMOUT_S
from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.messages.message_input import MessageInput
from pyOpticwash.waiting_input_data import WaitingInputData

BLOCKING_INPUT_SECONDS = 0.1


class Listener:
    def __init__(self, client: OpticwashCommands):
        self.client = client
        self.active = True
        self.thread: "threading.Thread" = threading.Thread(target=self.__listen)
        self.packet_timout = COMMAND_RECEIVING_TIMOUT_S
        self.waiting_input: list[WaitingInputData] = []
        self.processed_waiting_input: list[WaitingInputData] = []

    def start(self):
        self.thread.start()

    def __listen(self):
            ser: serial.Serial = self.client.get_serial()

            while self.active:
                try:
                    if not ser.in_waiting:
                        continue
                    try:
                        r = ser.read(1)
                        if r == b'\x02':
                            self.parse_new_message()
                            continue
                        logging.error(f"Failed to start a new message. Failed to read 0x02. Got {r}")
                    except serial.serialutil.SerialException as e:
                        time.sleep(1)
                        logging.error(f"Connection lost. Reconnecting.\"{e}\"")

                except Exception as e:
                    logging.exception(e)

    def parse_new_message(self):
        message = bytearray(1)
        message[0] = 0x02
        last_packet = time.time()
        ser: "serial.Serial" = self.client.get_serial()
        while len(message) <= 61:
            now = time.time()
            message.append(int.from_bytes(ser.read(1), 'big'))
            if now - last_packet > self.packet_timout:

                print("Timeout. Failed to receive a full message.")
                print(message)
                if message[-1] != 0x02:
                    print("Timeout. Failed to to start a new message.")
                    return
                return self.parse_new_message()
        if message[-1] != 0x03:
            print("Failed to find 0x03")
            return
        self._on_message_raw(message)

    def stop(self):
        self.active = False
        self.thread.join()

    def _on_message_raw(self, message_raw: bytearray):
        print("Message received:")
        for byte, i in zip(message_raw, range(len(message_raw))):
            print(f"{i}:{hex(byte)}", end=' ')
        print()
        try:
            message = MessageInput.unpack(message_raw)
            self._on_message(message)
        except ValueError as e:
            print(f"Failed to parse command: {e}")

    def _on_message(self, message: MessageInput):
        if self._try_process_waiting_input(message):
            return

        handler = HandlerDescriptor.get_handler(message.command, self.client)
        if handler:
            logging.debug("Handling message: " + handler.__class__.__name__)
            handler.handle(message)
        else:
            logging.info(f"No handler was found for {message.command}")

    def _try_process_waiting_input(self, message: MessageInput):
        to_be_processed = []

        for waiting_input in self.waiting_input:
            if waiting_input.try_set_result(message):
                to_be_processed.append(waiting_input)

        for waiting_input in to_be_processed:
            self.processed_waiting_input.append(waiting_input)
            self.waiting_input.remove(waiting_input)

        return len(to_be_processed) != 0

    def set_input(self, waiting_input: "WaitingInputData"):
        if (waiting_input in self.waiting_input or
                waiting_input in self.processed_waiting_input):
            raise ValueError("WaitingInputData is already in the queue or processed.")

        self.waiting_input.append(waiting_input)

    def get_input_blocking(self, waiting_input: "WaitingInputData") -> MessageInput | None:
        if waiting_input not in self.processed_waiting_input and waiting_input not in self.waiting_input:
            raise ValueError("WaitingInputData is not in the queue.")

        result = None
        time_waiting = 0

        while result is None:

            if time_waiting >= waiting_input.timeout:
                logging.info(f"Timeout while waiting for input {waiting_input}.")
                break

            result = waiting_input.get_result()
            time.sleep(BLOCKING_INPUT_SECONDS)
            time_waiting += BLOCKING_INPUT_SECONDS

        if waiting_input in self.processed_waiting_input:
            self.processed_waiting_input.remove(waiting_input)

        return result
