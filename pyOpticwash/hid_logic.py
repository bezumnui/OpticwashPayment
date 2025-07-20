"""
I've implement this logic because opticwash does not provide us the machine sources. After the user
chose the wash mode he will be prompted to swipe the card. And till the card is not swiped the machine won't accept any
signal from the RPI. This is because the display module is responsible for the card swipe. Silly, right? right.
My implementation is simple, I'm speaking to the small rp2040 controller which emulate the swipe signal.
"""
import logging
import serial

from config import UART_BAUNDRATE, UART_SWIPE_COMMAND, UART_SWIPE_APPROVAL, UART_MAX_ATTEMPTS


def try_send_to_rp2040_swipe():
    try:
        ser = serial.Serial("/dev/serial0", UART_BAUNDRATE, timeout=1)
        ser.write(UART_SWIPE_COMMAND)

        wait_for_answer = True
        attempt = 0
        while wait_for_answer:
            attempt += 1
            line = ser.read()

            if UART_SWIPE_APPROVAL in line:
                logging.info(f"Received: {line}")
                wait_for_answer = False
            else:
                logging.error(f"Failed to get response from rp2040 {attempt}/{UART_MAX_ATTEMPTS}. Got: \"{line}\"")

            if attempt >= UART_MAX_ATTEMPTS:
                logging.error(f"Failed to get response from rp2040.")
                return False

    except Exception as e:
        logging.exception(f"Failed to send to rp2040: {e}")
        return False

    return True
