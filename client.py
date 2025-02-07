import serial
import typing

from command import Command
from listener import Listener


class Opticwash:
    def __init__(self):
        self.ser: typing.Optional[serial.Serial] = None
        self.listener = Listener(self)
        self.packet_id = 0

    def open(self, port = '/dev/ttyACM0'):
        self.ser = serial.Serial(port, 9600)

    def listen(self):
        self.listener.start()

    def close(self):
        self.ser.close()

    def stop_listening(self):
        self.listener.stop()

    def send_command(self, command: Command):
        command.packet_label = self.packet_id & 0xFFFF
        self.packet_id += 1
        buffer = command.raw_command()
        self.ser.write(buffer)
        pass



    def open_cabinet(self):
        command = Command(6, 0, None, None, None)
        self.send_command(command)



    @staticmethod
    def print_buffer(buffer: bytearray):
        print("-----------------------------")
        for byte, i in zip(buffer, range(len(buffer))):
            print(f"{i}:{hex(byte)}", end=' ')



if __name__ == '__main__':
    opticwash = Opticwash()
    opticwash.open()
    opticwash.listen()
    input("Press enter to stop listening\n")

    opticwash.open_cabinet()
    opticwash.stop_listening()
    opticwash.close()
