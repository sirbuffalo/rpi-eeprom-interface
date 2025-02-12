import logging

from pi_to_eeprom_routines import initialize_pins_and_disable_chip, enable_led, disable_led, read_byte, write_byte, cleanup


logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    # level=logging.WARNING,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting read.py")

    try:
        initialize_pins_and_disable_chip()
        enable_led()

        address_data = [
            (0x0, 0b01010101),
            (0x1, 0b00000000),
            (0x2, 0b10011001),
            (0x3, 0b11101001),
            (0x4, 0b11110111),
            (0x5, 0b00100000),
            (0x6, 0b11011111),
            (0x7, 0b00001100),
        ]

        # write address_data 
        for address, byte_to_write in address_data:
            logger.debug(f'-- writing {byte_to_write:08b} - to address {address:#X}')
            write_byte(address, byte_to_write)

        # check proper writes
        for address, expected_byte in address_data:
            byte_read = read_byte(address)
            logger.debug(f'read value {byte_read:08b} from address {address:#X}')
            if byte_read != expected_byte:
                logger.warning(f'read value {byte_read:08b} from address {address:#X}, expected {expected_byte:08b}')

        # # read first 16 bytes
        # for address in range(0x0, 0x10):
        #     byte_read = read_byte(address)
        #     logger.info(f'read value {byte_read:08b} from address {address:#X}')
    except KeyboardInterrupt:
        logger.info("Recieved KeyboardInterrupt")
    except Exception as e:
        logger.error("ERROR: ", e)
    finally:
        logger.info("Cleaning up...")
        disable_led()
        cleanup()


if __name__ == "__main__":
    main()