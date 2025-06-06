import logging

from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.handler import OpticwashInputHandler
from pyOpticwash.handler_descriptor import HandlerDescriptor
from pyOpticwash.handlers.screen_id import ScreenID
from pyOpticwash.handlers.system_error_code import SystemErrorCode
from pyOpticwash.hid_logic import send_to_rp2040_swipe
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
            send_to_rp2040_swipe()
            self.base.state.set_state(OpticwashState.TransactionWaitingRealCard)
            self.base.keep_alive()

        elif current_screen == ScreenID.Standby:
            self.base.state.set_state(OpticwashState.Standby)
