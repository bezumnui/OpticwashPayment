import time

import typing

from threading import Thread


class TimeoutWatchdog:
    def __init__(self, callback: typing.Callable, seconds: int):
        self.__seconds = seconds
        self.thread: Thread | None = None
        self.callback: typing.Callable = callback
        self.working = False

    def start(self):
        self.thread = Thread(target=self.__schedule_callback)
        self.thread.start()
        self.working = True

    def stop(self):
        if self.thread is not None:
            self.working = False
            self.thread = None

    def __should_continue_watching(self) -> bool:
        return self.callback() if self.callback else True

    def __schedule_callback(self):
        time.sleep(self.__seconds)

        if self.working:
            self.callback()
