from pyOpticwash.client import PyOpticwash

if __name__ == '__main__':
    opticwash = PyOpticwash()
    opticwash.start()
    opticwash.keep_alive()
    input("Press enter to stop listening\n")

    # opticwash.open_cabinet()
    opticwash.keep_alive()
    opticwash.stop()
