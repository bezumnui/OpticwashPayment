from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    opticwash = PyOpticwash()
    opticwash.start()
    opticwash.mdb_client.send_raw("R,18")
    while True:
        pass