from enum import Enum, auto


class SystemErrorCode(Enum):
    Ok = 0
    CabinetDoorOpened = auto()
    CabinetDoorUnlocked = auto()
    InitializeError = auto()
    DCModuleFailed = auto()
    ACModuleFailed = auto()
    DisplayControllerFailed = auto()
    SystemMemoryFailed = auto()
    CabinetFlood = auto()
    DoorMotorErrorOpen = auto()
    DoorMotorErrorClose = auto()
    ClampError = auto()
    UnclampError = auto()
    StepperHomingError = auto()
    TankEmpty = auto()
    WashPumpPressureLimit = auto()
    Jam = auto()
    BottleEmpty = auto()
    ReservoirTimeout = auto()
    TDSHighLimit = auto()
    CashAcceptorError = auto()
    CardReaderDetached = auto()