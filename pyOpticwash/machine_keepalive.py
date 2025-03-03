import logging
import threading

import schedule

from pyOpticwash.commands import OpticwashCommands
from pyOpticwash.finite_state_machine import OpticwashState


class OpticwashScheduler:
    def __init__(self, client: OpticwashCommands):
        self.client = client
        self.active = False
        self._thread = threading.Thread(target=self.__poll_scheduler)
        self._keep_alive_job = None


    def keepalive(self):
        if not self._keep_alive_job:
            self._keep_alive_job = schedule.every(5).seconds.do(self.keepalive)

        if self.client.state in (OpticwashState.TransactionWaitingRealCard, OpticwashState.TransactionWaitingApproval):
            logging.debug("Sending keep alive")
            self.client.send_keep_transaction_alive()
        else:
            schedule.cancel_job(self._keep_alive_job)
            self._keep_alive_job = None

    def __poll_scheduler(self):
        while self.active:
            schedule.run_pending()

    def start_scheduler(self):
        self.active = True
        self._thread.start()

    def stop_scheduler(self):
        self.active = False
        self._thread.join()

