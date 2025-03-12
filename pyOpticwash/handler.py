import abc

from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.messages.message_input import MessageInput
from pyOpticwash.opticwash_base import OpticwashBase



class OpticwashInputHandler(abc.ABC):

    def __init__(self, base: OpticwashCommands):
        self.base = base

    @abc.abstractmethod
    def handle(self, message: MessageInput):
        raise NotImplementedError()


