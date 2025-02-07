import serial
import typing

from command import Command
from listener import Listener


class Opticwash:
    def __init__(self):
        self.ser: typing.Optional[serial.Serial] = None
        self.listener = Listener(self)

    def open(self, port = '/dev/ttyACM0'):
        self.ser = serial.Serial(port, 9600)

    def listen(self):
        self.listener.start()

    def close(self):
        self.ser.close()

    def stop_listening(self):
        self.listener.stop()

    def send_command(self, command: Command):
        buffer = command.raw_command()
        self.ser.write(buffer)
        pass


    def open_cabinet(self):
        command = Command(6, 0, None, None, None)
        self.send_command(command)



    @staticmethod
    def print_buffer(buffer: bytearray):
        for byte, i in zip(buffer, range(len(buffer))):
            print(f"{i}:{hex(byte)}", end=' ')



if __name__ == '__main__':
    opticwash = Opticwash()
    opticwash.open()
    opticwash.listen()
    opticwash.open_cabinet()
    input("Press enter to stop listening")
    opticwash.stop_listening()
    opticwash.close()
