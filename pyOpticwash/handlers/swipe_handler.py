import logging
import threading

import time
from enum import Enum, auto


from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.handler import OpticwashInputHandler
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.messages.message import CommandCode
from pyOpticwash.messages.message_input import MessageInput

CENTS_TO_CASH = 100


# Controller requests transaction approval after a card is swiped.
# It will timeout in 20 seconds if there is nothing coming back from the PI

# Byte 1 (Amount): 0-255
# Byte 2 (Wash Type): 0 eyewear, 1 jewelry, and 2 phone
# Byte 3 (Payment Type): 0 free, 1 cash, 2 loyalty card, 3 credit card
# If it's credit card, byte 4 to byte 43 is 40-byte track2 data
# If it's loyalty card, byte 4 to byte 19 is 16-byte loyalty card number


class WashType(Enum):
    eyewear = 0
    jewelry = auto()
    phone = auto()


class PaymentType(Enum):
    free = 0
    cash = auto()
    loyalty = auto()
    card = auto()


class Prices:
    eyewear = 2000
    jewelry = 2500
    phone = 500

    @classmethod
    def get_price(cls, wash_type: WashType):
        if wash_type == WashType.eyewear:
            return cls.eyewear
        elif wash_type == WashType.jewelry:
            return cls.jewelry
        elif wash_type == WashType.phone:
            return cls.phone
        else:
            raise ValueError("Invalid wash type")


@HandlerDescriptor.register(CommandCode.Command)
class SwipeHandler(OpticwashInputHandler):
    HARDCODED_AMOUNT = 1

    def approve_received(self):
        self.base.approve_transaction()
        self.base.state.set_state(OpticwashState.TransactionApproval)


    def reject_received(self):
        self.base.decline_transaction()
        self.base.state.set_state(OpticwashState.Standby)

    def handle(self, message: MessageInput):
        amount = message.data[0]
        wash_type = WashType(message.data[1])
        payment_type = PaymentType(message.data[2])
        logging.info(f"SwipeHandler: wash: {wash_type.name}, payment: {payment_type.name}, amount: {amount}")

        # if self.base.state != OpticwashState.TransactionWaitingRealCard and BYPASS_INSERT_STATE == False:
        #     return False

        logging.info("Тут мы готовим терминал...")
        self.base.state.set_state(OpticwashState.TransactionWaitingApproval)
        self.base.keep_alive()
        mdb = self.base.get_raw_mdb()

        mdb.set_success_callback(self.approve_received)
        mdb.set_fail_callback(self.reject_received)

        # if not mdb.request_vending(amount * CENTS_TO_CASH):
        if not mdb.request_vending(SwipeHandler.HARDCODED_AMOUNT * CENTS_TO_CASH):
            return self.reject_received()


        self.terminal_lookup(120)

    def terminal_lookup(self, total_time: int):
        end_time = time.time() + total_time

        def lookup():
            while time.time() < end_time:
                if self.base.state != OpticwashState.TransactionWaitingApproval:
                    logging.info("terminal_lookup: Transaction is no longer waiting for approval")
                    return
                time.sleep(1)
            logging.info("terminal_lookup: Timeout reached")
            mdb = self.base.get_raw_mdb()
            mdb.request_reset()
            self.reject_received()

        threading.Thread(target=lookup).start()
