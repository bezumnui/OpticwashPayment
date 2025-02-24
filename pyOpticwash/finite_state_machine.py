from enum import Enum, auto


class OpticwashState(Enum):
    Unknown = -1
    Standby = auto()
    WaitingMagnetCard = auto()
    TransactionCancelled = auto()
    TransactionWaitingRealCard = auto()
    TransactionWaitingApproval = auto()
    TransactionApproval = auto()





class FSMState:
    def __init__(self, state: Enum):
        self.state = state
        self._data = {}

    def update_date(self, value: dict):
        self._data.update(value)

    def get_data(self, key: dict):
        return self._data.get(key, None)

    def set_state(self, state: Enum):
        self.state = state

    def __eq__(self, other: "Enum"):
        if not isinstance(other, Enum):
            raise ValueError(f"Could not check equality with {other.__class__}. Waiting for {Enum.__class__}")
        return self.state == other



# FSMState.set_state(state)
# FSMState == state
