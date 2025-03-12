import logging
import threading
import time

from pyOpticwash.commands import OpticwashCommands
from py_mdb_terminal.mdb_client import MDBClient
from serial.tools import list_ports


def check_p_ack(data: str):
    return data.lower().split(",")[1] == "ack"


class __RawMDBListener:
    def __init__(self, opticwash: OpticwashCommands):
        self.opticwash = opticwash
        self.working = False
        self.thread = threading.Thread(target=self.__poll_processing)
        self.polling_filters = []

    def start_polling(self):
        self.working = True
        self.thread.start()

    def stop_polling(self):
        self.working = False
        self.thread.join()


    def success_payment(self):
        self.mdb.send_raw_message_with_response("R,13,02ffff".encode(self.mdb.get_encoding()))
        time.sleep(1)
        self.mdb.send_raw_message_with_response("R,13,04".encode(self.mdb.encoding))

    def cancel_payment(self):
        self.mdb.send_raw_message_with_response("R,13,01".encode(self.mdb.get_encoding()))
        time.sleep(1)
        self.mdb.send_raw_message_with_response("R,13,04".encode(self.mdb.encoding))

    def fail_payment(self):
        self.mdb.send_raw_message_with_response("R,13,03".encode(self.mdb.get_encoding()))
        time.sleep(1)
        self.mdb.send_raw_message_with_response("R,13,04".encode(self.mdb.encoding))


    def wait_for_poll_answer(self, message_start_with: str):
        waiting = True
        def filter(data: str):
            nonlocal waiting
            if data.split(",")[1].startswith(message_start_with):
                self.polling_filters.remove(filter)
                waiting = False

        self.polling_filters.append(filter)
        while waiting:
            time.sleep(.1)
        return


    def __poll_processing(self):
        while self.working:
            time.sleep(5)
            r = self.mdb.send_raw_message_with_response("R,12".encode(self.mdb.encoding))
            for filter in self.polling_filters:
                filter(r)
            message = r.split(",")
            if len(message) < 2:
                continue
            if message[1].startswith("05"):
                print(f"Successfully paid {int(message[1][2:], 16)} AED")
                time.sleep(1)
                self.success_payment()


            elif message[1].startswith("06"):
                print(f"Failed to pay. Error: {message[1][2:]}")
                # mdb.send_raw_message_with_response("R,12,00".encode(mdb.encoding))


            # mdb.send_raw_message_with_response("R,12,0264Thank you!".encode(mdb.get_encoding()))

    def request_vending(self, amount: int):
        if not check_p_ack(self.mdb.send_raw_message_with_response("M,1".encode(self.mdb.get_encoding()))):
            print("M, 1 error")
            return

        if not check_p_ack(self.mdb.send_raw_message_with_response("R,14,01".encode(self.mdb.get_encoding()))):
            print("Reader mode error")
            return

        self.wait_for_poll_answer("03")

        amount_hex = hex(amount & 0xFFFF)[2:]
        amount_hex = "0" * (4 - len(amount_hex)) + amount_hex

        if not check_p_ack(self.mdb.send_raw_message_with_response(f"R,13,00{amount_hex}ffff".encode(self.mdb.get_encoding()))):
            print("vending error")
            return
        print("requested")


    def success_handler(self):
       pass

    def fail_handler(self):
        pass


if __name__ == '__main__':
    device_list = list_ports.comports()
    for device in device_list:

        print(device.pid, device.vid, device.device)
    # logging.basicConfig(level=logging.DEBUG)
    # client = MDBClient("/dev/tty.usbmodem01")
    # client.start()
    # listener = RawMDBListener(client)
    # listener.start_polling()
    # while True:
    #     menu = input("input 1 to creadit")
    #     if menu == "1":
    #         listener.request_vending(20)
    #     if not menu:
    #         listener.stop_polling()
    #         break
    #     else:
    #         client.send_raw_message(menu.encode(client.get_encoding()))

# R,11,0001130500000001
# R,12,0210hello