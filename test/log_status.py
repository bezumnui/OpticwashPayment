import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.misc.utils import get_mdb_by_vendor

if __name__ == '__main__':
    opticwash = PyOpticwash()
    opticwash.start_machine(get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID))
    opticwash.request_status()
