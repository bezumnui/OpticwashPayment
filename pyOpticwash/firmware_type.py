import enum


class FirmwareType(enum.Enum):
    AC_Module = enum.auto()
    DC_Module = enum.auto()
    Display_Module = enum.auto()

    @staticmethod
    def get_address(firmware_type: 'FirmwareType') -> int:
        if firmware_type == FirmwareType.AC_Module:
            return 3
        elif firmware_type == FirmwareType.DC_Module:
            return 2
        elif firmware_type == FirmwareType.Display_Module:
            return 1
        else:
            raise ValueError("Invalid firmware type")