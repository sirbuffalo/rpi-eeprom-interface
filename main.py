import logging

from eeprom import EEPROM
from json import dumps


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    address_data = {
        0x0: 0b01010101,
        0x1: 0b00000000,
        0x2: 0b10011001,
        0x3: 0b11101001,
        0x4: 0b11110111,
        0x5: 0b00100000,
        0x6: 0b11011111,
        0x7: 0b00001100
    }

    logger.info(f'Writing {len(address_data)} bytes...')

    with EEPROM() as eeprom:
        eeprom.write_bytes(address_data)
        eeprom.check_bytes(address_data)
        print('\n'.join([f'{address:011b}: {byte:08b}' for address, byte in eeprom.read_bytes(range(0x20)).items()]))

    logger.info(f'Write complete.')


if __name__ == '__main__':
    main()
