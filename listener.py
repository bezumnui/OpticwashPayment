import threading
import time

import serial


class Listener:
    def __init__(self, client: "Opticwash"):
        self.client = client
        self.active = True
        self.thread: "threading.Thread" = threading.Thread(target=self.__listen)
        self.packet_timout = 0.5

    def start(self):
        self.thread.start()

    def __listen(self):
        ser: serial.Serial = self.client.ser

        while self.active:
            r = ser.read(1)
            if r == b'\x02':
                self.parse_new_message()
                continue
            print(f"Failed to start a new message. Failed to read 0x02. Got {r}")


    def parse_new_message(self):
        message = bytearray(1)
        message[0] = 0x02
        last_packet = time.time()
        ser: "serial.Serial" = self.client.ser
        while message[-1] != 0x03:
            now = time.time()
            message.append(int.from_bytes(ser.read(1), 'big'))
            if now - last_packet > self.packet_timout:
                print("Timeout. Failed to receive a full message.")
                if message[-1] != 0x02:
                    print("Timeout. Failed to to start a new message.")
                    return
                return self.parse_new_message()
        self._on_message(message)



    def stop(self):
        self.active = False
        self.thread.join()

    def _on_message(self, message: bytearray):
        print("Message received:")
        for byte, i in zip(message, range(len(message))):
            print(f"{i}:{hex(byte)}", end=' ')
        print()