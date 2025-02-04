import logging

from time import sleep

from pin_setup import address_pins, data_pins, test_led

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)


def set_address(address):
    for pin, value in zip(address_pins, f'{address:011b}'):
        if int(value):
            pin.on()
        else:
            pin.off()


def set_data(data):
    for pin, value in zip(data_pins, f'{data:08b}'):
        if int(value):
            pin.on()
        else:
            pin.off()


def main():
    logger.info("Entering main()")

    while True:
        logger.debug("New blink cycle...")
        test_led.on()
        sleep(1)
        test_led.off()
        sleep(1)


if __name__ == "__main__":
    main()