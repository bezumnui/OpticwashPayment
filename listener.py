import threading
import typing


class Listener:
    def __init__(self, client: "Opticwash"):
        self.client = client
        self.active = True
        self.thread: "threading.Thread" = threading.Thread(target=self.__listen)

    def start(self):
        self.thread.start()

    def __listen(self):
        while self.active:
            buffer = self.client.ser.read(64)
            self._on_message(buffer)

    def stop(self):
        self.active = False
        self.thread.join()

    def _on_message(self, message: bytearray):
        for byte, i in zip(message, range(len(message))):
            print(f"{i}:{hex(byte)}", end=' ')
        print()