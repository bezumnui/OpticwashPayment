
if __name__ == '__main__':
    from pyOpticwash.client import PyOpticwash

    opticwash = PyOpticwash()
    opticwash.start_mdb()
    opticwash.open_cabinet()
    opticwash.stop()
