import threading
import time

import serial

from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.messages.message_input import MessageInput


class Listener:
    def __init__(self, client: OpticwashCommands):
        self.client = client
        self.active = True
        self.thread: "threading.Thread" = threading.Thread(target=self.__listen)
        self.packet_timout = 0.5

    def start(self):
        self.thread.start()

    def __listen(self):
        ser: serial.Serial = self.client.get_serial()

        while self.active:
            if not ser.in_waiting:
                continue
            r = ser.read(1)
            if r == b'\x02':
                self.parse_new_message()
                continue
            print(f"Failed to start a new message. Failed to read 0x02. Got {r}")

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
        handler = HandlerDescriptor.get_handler(message.command, self.client)
        if handler:
            handler.handle(message)