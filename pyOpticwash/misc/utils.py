from serial.tools import list_ports


def get_mdb_by_vendor(vendor: str) -> str | None:
    device_list = list_ports.comports()
    for device in device_list:
        if device.vid == vendor:
            return device.device