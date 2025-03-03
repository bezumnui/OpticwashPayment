import logging

from pyOpticwash.handler import OpticwashInputHandler
from pyOpticwash.messages.message import CommandCode
from pyOpticwash.opticwash_base import OpticwashBase


class HandlerDescriptor:
    _register: dict[CommandCode, type[OpticwashInputHandler]] = {}

    @classmethod
    def register(cls, command: CommandCode):
        """
        Use as a decorator for a class to register the handler
        :param command: command from `MessageInput`
        """
        def decorator(handler_cls: type[OpticwashInputHandler]):
            cls._register.update({command: handler_cls})
            return handler_cls
        return decorator

    @classmethod
    def get_handler(cls, code: CommandCode, base: OpticwashBase):
        logging.info(str(cls._register))
        handler_cls  = cls._register.get(code, None)

        if not handler_cls:
            raise ValueError(f"No handler for {code.name}")
        return handler_cls(base)
