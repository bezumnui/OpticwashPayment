import logging
from enum import Enum, auto

from py_mdb_terminal.commands.structures.slave.cashless_slave_answer import CashlessError

from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.handlers.handler import OpticwashInputHandler
from pyOpticwash.handlers.handler_descriptor import HandlerDescriptor
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

    def start_session(self, price: int):
        answer, res = self.base.get_mdb_client().start_session(price)
        return self.handle_error(answer, res)

    def approve_request(self, price: int):
        answer, res = self.base.get_mdb_client().approve_vending_request(price)
        return self.handle_error(answer, res)

    def handle_error(self, answer: CashlessError | None, res: str):
        logging.info(f"Got response: {answer.name}")
        if isinstance(answer, CashlessError):
            logging.error(f"Got error on response: {answer.name}, ({res}). Resetting...")
            self.base.get_mdb_client().reset_reboot()
            self.base.state.set_state(OpticwashState.Standby)
            return False
        return True

    def handle(self, message: MessageInput):
        if self.base.state != OpticwashState.TransactionWaitingRealCard:
            return False

        amount = message.data[0]
        wash_type = WashType(message.data[1])
        payment_type = PaymentType(message.data[2])
        price = int(amount * 100)

        logging.info(f"SwipeHandler: wash: {wash_type.name}, payment: {payment_type.name}, amount: {amount}")

        if not self.start_session(price):
            return True
        if not self.approve_request(price):
            return True

        self.base.state.set_state(OpticwashState.TransactionWaitingApproval)




