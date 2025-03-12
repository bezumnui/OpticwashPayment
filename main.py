import logging

import config
from pyOpticwash.client import PyOpticwash
from pyOpticwash.finite_state_machine import OpticwashState
from pyOpticwash.misc.utils import get_mdb_by_vendor

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    port = get_mdb_by_vendor(config.AC_MODULE_VENDOR_ID)
    opticwash = PyOpticwash()
    opticwash.start()
    input()
    opticwash.stop()
