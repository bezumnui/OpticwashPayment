import logging
import threading

import time
from enum import Enum, auto

from py_mdb_terminal.commands.structures.slave.cashless_slave_answer import CashlessError

from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.handler import OpticwashInputHandler
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.messages.message import CommandCode
from pyOpticwash.messages.message_input import MessageInput


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


@HandlerDescriptor.register(CommandCode.Swipe)
class SwipeHandler(OpticwashInputHandler):



    def approve_received(self):
        self.base.approve_transaction()
        self.base.state.set_state(OpticwashState.TransactionApproval)


    def reject_received(self):
        self.base.decline_transaction()
        self.base.state.set_state(OpticwashState.Standby)

    def handle(self, message: MessageInput):
        if self.base.state != OpticwashState.TransactionWaitingRealCard:
            return False

        amount = message.data[0]
        wash_type = WashType(message.data[1])
        payment_type = PaymentType(message.data[2])

        logging.info(f"SwipeHandler: wash: {wash_type.name}, payment: {payment_type.name}, amount: {amount}")

        logging.info("Тут мы готовим терминал...")
        self.base.state.set_state(OpticwashState.TransactionWaitingApproval)
        self.base.keep_alive()
        mdb = self.base.get_raw_mdb()

        mdb.set_success_callback(self.approve_received)
        mdb.set_fail_callback(self.reject_received)
        if wash_type == wash_type.eyewear:
            mdb.request_vending(20)
        elif wash_type == wash_type.jewelry:
            mdb.request_vending(25)
        else:
            mdb.request_vending(5)
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
