from queue import Empty

from logging.handlers import RotatingFileHandler

import os

from datetime import datetime

import logging
import threading
import time

import config
from pyOpticwash.misc.utils import get_mdb_by_vendor
from py_mdb_terminal.mdb_client import MDBClient


def check_p_ack(data: str):
    # print(data.lower().split(",")[1], "ack", data.lower().split(",")[1] == "ack")
    # return data.lower().split(",")[1] == "ack"
    return "ack" in data.lower()


class RawMDBListener:
    def __init__(self):
        device = get_mdb_by_vendor(config.TERMINAL_VENDOR_ID)
        if not device:
            raise Exception("MDB device not found")

        self.mdb = MDBClient(device)
        self.working = False
        self.thread = threading.Thread(target=self.__poll_processing)
        self.polling_filters = []
        self.success_callback = None
        self.fail_callback = None
        self.__loop_delay = 0.1

        self.__logger = logging.getLogger(RawMDBListener.__name__)
        self.__setup_logging()

    def __setup_logging(self):
        self.__logger.setLevel(logging.DEBUG)

        if not os.path.exists("log"):
            os.mkdir("log")

        file_handler = RotatingFileHandler(
            filename=datetime.now().strftime("log/mdb_listener_log_%d.%m.%Y_%H.%M.%S"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )

        stream_handler = logging.StreamHandler()

        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)


    def start(self):
        self.mdb.start()

    def stop(self):
        self.mdb.stop()

    def set_success_callback(self, callback):
        self.success_callback = callback

    def set_fail_callback(self, callback):
        self.fail_callback = callback

    def start_polling(self):
        self.working = True

        if not check_p_ack(self.mdb.send_raw_message_with_response("M,1".encode(self.mdb.get_encoding()))):
            self.__logger.error("M, 1 error")
            return

        self.__logger.info("MDB, manual mode.")

        self.thread.start()

    def reset(self):
        self.mdb.send_raw_message("F,RESET".encode(self.mdb.get_encoding()))

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

    def __log_telemetry(self, ):
        ...

    def __poll_processing(self):
        while self.working:
            time.sleep(self.__loop_delay)
            try:
                r = self.mdb.send_raw_message_with_response("R,12".encode(self.mdb.encoding))
            except Empty:
                logging.info("Polling timeout. Retrying...")
                continue

            for filter in self.polling_filters:
                filter(r)

            message = r.split(",")

            if len(message) < 2:
                continue

            if message[1].startswith("05"):
                self.__logger.info(f"Successfully paid {int(message[1][2:], 16)} AED")
                self.success_payment()
                self.success_callback()

            elif message[1].startswith("06"):
                self.__logger.error(f"Failed to pay. Error: {message[1][2:]}")

                self.fail_payment()
                self.fail_callback()

    def request_reset(self):
        self.mdb.send_raw("R,10".encode(self.mdb.get_encoding()))

    def request_vending(self, amount: int):

        response = self.mdb.send_raw_message_with_response("R,14,01".encode(self.mdb.get_encoding()));
        if not check_p_ack(response):
            self.__logger.error("Reader mode error")

            return False

        # self.wait_for_poll_answer("03")
        time.sleep(0.2)

        amount_hex = hex(amount & 0xFFFF)[2:]
        amount_hex = "0" * (4 - len(amount_hex)) + amount_hex

        if not check_p_ack(
                self.mdb.send_raw_message_with_response(f"R,13,00{amount_hex}ffff".encode(self.mdb.get_encoding()))):
            self.__logger.error("Vending error")
            return False

        return True

