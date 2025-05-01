import logging

from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opticwash = PyOpticwash()
    # opticwash.raw_mdb.request_vending()
    opticwash.raw_mdb.start_polling()
    opticwash.raw_mdb.request_vending(10)
    while True:
        print(opticwash.raw_mdb.mdb.send_raw_message_with_response(input().encode()))
        input("Press enter...")
