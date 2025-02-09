import logging

from pi_to_eeprom_routines import initialize_pins_and_disable_chip, enable_led, disable_led, read, write, cleanup


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting read.py")

    try:
        initialize_pins_and_disable_chip()
        enable_led()

        # read()
        write(0, 0)

        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Recieved KeyboardInterrupt")
    finally:
        logger.info("Cleaning up...")
        disable_led()
        cleanup()


if __name__ == "__main__":
    main()