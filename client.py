import serial
import typing

from command import Command


class Opticwash:
    def __init__(self):
        self.ser: typing.Optional[serial.Serial] = None

    def open(self, port = '/dev/ttyACM0'):
        self.ser = serial.Serial(port, 9600)

    def close(self):
        self.ser.close()

    def send_command(self, command: Command):
        buffer = command.raw_command()
        self.ser.write(buffer)
        pass


    def open_cabinet(self):
        command = Command(6, 0, None, None, None)
        self.send_command(command)
        # buffer = bytearray(0)
        # buffer.append(0x02) # start tx 1
        #
        # buffer.append(0x00) # address 2
        # buffer.append(0x00) # 3
        #
        # buffer.append(0x00) # packet label 4
        # buffer.append(0x00) #  5
        #
        # buffer.append(0x06) # command 6
        # buffer.append(0x00) # packet type 7
        #
        # buffer.append(0x32) # data length 8
        # buffer.append(0x00) # 9
        #
        # for i in range(0, 50):
        #     buffer.append(0x00) # data 10-59
        #
        # buffer.append(self.calculate_checksum(buffer[:59])) # checksum 60
        # buffer.append(0x03) # end tx 61
        # self.print_buffer(buffer)
        # self.send_command(buffer)
        pass



    @staticmethod
    def print_buffer(buffer: bytearray):
        for byte, i in zip(buffer, range(len(buffer))):
            print(f"{i}:{hex(byte)}", end=' ')



if __name__ == '__main__':
    opticwash = Opticwash()
    opticwash.open()
    opticwash.open_cabinet()
    opticwash.close()