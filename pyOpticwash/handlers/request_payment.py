import logging
import threading
import time

import config
from pyOpticwash.misc.utils import get_mdb_by_vendor
from py_mdb_terminal.mdb_client import MDBClient



def check_p_ack(data: str):
    return data.lower().split(",")[1] == "ack"



class RawMDBListener:
    def __init__(self, opticwash):
        device = get_mdb_by_vendor(config.TERMINAL_VENDOR_ID)
        if not device:
            raise Exception("MDB device not found")

        self.mdb = MDBClient(device)
        self.mdb.start()
        self.working = False
        self.thread = threading.Thread(target=self.__poll_processing)
        self.polling_filters = []
        self.success_callback = None
        self.fail_callback = None

    def set_success_callback(self, callback):
        self.success_callback = callback

    def set_fail_callback(self, callback):
        self.fail_callback = callback


    def start_polling(self):
        self.working = True
        self.thread.start()

    def stop_polling(self):
        self.working = False
        self.thread.join()


    def success_payment(self):
        time.sleep(1)
        self.mdb.send_raw_message_with_response("R,13,02ffff".encode(self.mdb.get_encoding()))
        time.sleep(1)
        self.mdb.send_raw_message_with_response("R,13,04".encode(self.mdb.encoding))

    def cancel_payment(self):
        time.sleep(1)
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
                self.success_payment()
                self.success_callback()


            elif message[1].startswith("06"):
                print(f"Failed to pay. Error: {message[1][2:]}")
                self.fail_payment()
                self.fail_callback()



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

