import threading

import time

import typing

import logging

from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.handler import OpticwashInputHandler
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.handlers.screen_id import ScreenID
from pyOpticwash.handlers.system_error_code import SystemErrorCode
from pyOpticwash.hid_logic import try_send_to_rp2040_swipe
from pyOpticwash.messages.message import CommandCode
from pyOpticwash.messages.message_input import MessageInput


@HandlerDescriptor.register(CommandCode.Status)
class StatusHandler(OpticwashInputHandler):

    def handle(self, message: MessageInput):
        system_error_code = SystemErrorCode(message.data[0])
        current_screen = ScreenID(message.data[1])
        _msb, _lsb = message.data[2:4]
        price_eyewear = message.data[4]
        price_jewelry = message.data[5]
        price_phone = message.data[6]

        logging.info(
            f"Received StatusHandler: {system_error_code.name}, {current_screen.name}, price: {price_eyewear}, {price_jewelry}, {price_phone}")

        if current_screen == ScreenID.InsertCashOrCard:
            self.do_with_repetition_in_thread(try_send_to_rp2040_swipe, 1, 5)
            # if try_send_to_rp2040_swipe() == False:
            #     pass
            #     self.base.cancel_transaction()
            #     return

            self.base.state.set_state(OpticwashState.TransactionWaitingRealCard)
            self.base.keep_alive()

        elif current_screen == ScreenID.Standby:
            self.base.state.set_state(OpticwashState.Standby)
    #

    def do_with_repetition_in_thread(self, func: typing.Callable, delay_seconds: int, repeats: int = 1):
        thread = threading.Thread(target=self.do_with_repetition, args=(func, delay_seconds, repeats))
        thread.start()

    @staticmethod
    def do_with_repetition(func: typing.Callable, delay_seconds, repeats: int):
        for i in range(repeats - 1):
            func()
            time.sleep(delay_seconds)

        if repeats > 0:
            func()

@HandlerDescriptor.register(CommandCode.RequestStatus)
class StatusRequestedHandler(OpticwashInputHandler):


    def handle(self, message: MessageInput):
        self.parse_status(message.data)


    def parse_status(self, data: bytes) -> None:
        ERROR_CODES = {
            0: "OK",
            2: "Invalid command, resend",
            3: "Invalid packet, resend",
        }

        if len(data) < 21:
            raise ValueError("need ≥ 21 bytes")

        # versions
        display_hw, display_fw, dc_hw, dc_fw, ac_hw, ac_fw, sys_err = data[:7]

        # cash (big-endian 16-bit)
        cash = (data[7] << 8) | data[8]

        # 24-bit serials
        disp_esn = (data[9] << 8) | (data[10] << 8) | data[11]
        dc_esn = (data[12] << 8) | (data[13] << 8) | data[14]
        ac_esn = (data[15] << 8) | (data[16] << 8) | data[17]

        eyewear_price, jewelry_price, phone_price = data[18:21]

        print(f"Display HW ver: {display_hw}")
        print(f"Display FW ver: {display_fw}")
        print(f"DC HW ver: {dc_hw}")
        print(f"DC FW ver: {dc_fw}")
        print(f"AC HW ver: {ac_hw}")
        print(f"AC FW ver: {ac_fw}")

        print(f"System error: {sys_err} ({ERROR_CODES.get(sys_err, 'unknown')})")

        print(f"Cash in bill acceptor: {cash}")
        print(f"Display ESN: 0x{disp_esn:06X} ({disp_esn})")
        print(f"DC ESN:      0x{dc_esn:06X}")
        print(f"AC ESN:      0x{ac_esn:06X}")

        print(f"Eyewear price: {eyewear_price}")
        print(f"Jewelry price: {jewelry_price}")
        print(f"Phone price:   {phone_price}")
