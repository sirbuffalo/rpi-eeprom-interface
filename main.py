import logging

from eeprom import EEPROM
from json import dumps


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)


def test_write():
    address_data = {
        0x0: 0b01010101,
        0x1: 0b00000000,
        0x2: 0b10011001,
        0x3: 0b11101001,
        0x4: 0b11110111,
        0x5: 0b00100000,
        0x6: 0b11011111,
        0x7: 0b00001100,
        0x8: 0b01010101,
        0x9: 0b00000000,
        0xA: 0b10011001,
        0xB: 0b11101001,
        0xC: 0b11110111,
        0xD: 0b00100000,
        0xE: 0b11011111,
        0xF: 0b00001100
    }
    address_data = {x: 0xFF for x in range(0x10)}
    logger.info(f'Writing {len(address_data)} bytes...')

    with EEPROM() as eeprom:
        eeprom.write_bytes(address_data)
        eeprom.check_bytes(address_data)

    logger.info(f'Write complete.')

def read(start_address: int, length: int):
    with EEPROM() as eeprom:
        print('\n'.join([f'{address:011b}: {byte:08b}' for address, byte in eeprom.read_bytes(range(start_address, start_address + length)).items()]))

def main():
    # test_write()
    read(0, 0x40)


if __name__ == '__main__':
    main()
