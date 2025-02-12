import logging
from time import sleep
from typing import Iterable

import support_testing_off_pi  # noqa: F401
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class EEPROM:
    ADDRESS_PINS: tuple[int] = (4, 17, 27, 22, 10, 9, 11, 5, 14, 15, 24)
    DATA_PINS: tuple[int] = (6, 13, 19, 20, 16, 12, 7, 8)

    WE_PIN: int = 18
    OE_PIN: int = 23
    CE_PIN: int = 25

    ADDRESS_CE_OE_TO_OUTPUT_DELAY = 0.000000150
    OUTPUT_DISABLE_DELAY = 0.000000050
    ADDRESS_TO_WE_PULSE_START_DELAY = 0.000000010
    WRITE_CYCLE_DELAY = 0.001

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(EEPROM.WE_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(EEPROM.OE_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(EEPROM.CE_PIN, GPIO.OUT, initial=GPIO.HIGH)

        GPIO.setup(EEPROM.ADDRESS_PINS, GPIO.OUT, initial=GPIO.LOW)

    def __enter__(self):
        return self

    def set_gpio_data_pins_to_read(self):
        GPIO.setup(EEPROM.DATA_PINS, GPIO.IN)

    def set_gpio_data_pins_to_write(self):
        GPIO.setup(EEPROM.DATA_PINS, GPIO.OUT)

    def set_address(self, address: int):
        assert isinstance(address, int)
        assert 0 <= address < (1 << 11)

        address_pin_values = tuple(EEPROM.bool_to_high_low(int(pin_value)) for pin_value in f'{address:011b}')
        GPIO.output(EEPROM.ADDRESS_PINS, address_pin_values)

    def set_data(self, data: int):
        assert isinstance(data, int)
        assert 0 <= data < (1 << 8)

        data_pin_values = tuple(EEPROM.bool_to_high_low(int(pin_value)) for pin_value in f'{data:08b}')
        GPIO.output(EEPROM.DATA_PINS, data_pin_values)

    def read_data(self) -> int:
        byte = 0
        for pin_number in EEPROM.DATA_PINS:
            byte = (byte << 1) | GPIO.input(pin_number)

        assert 0 <= byte < (1 << 8)
        return byte

    def read_byte(self, address: int):
        GPIO.output(EEPROM.WE_PIN, GPIO.HIGH)

        self.set_address(address)

        self.set_gpio_data_pins_to_read()
        GPIO.output(EEPROM.CE_PIN, GPIO.LOW)
        GPIO.output(EEPROM.OE_PIN, GPIO.LOW)

        sleep(EEPROM.ADDRESS_CE_OE_TO_OUTPUT_DELAY)

        byte = self.read_data()

        GPIO.output(EEPROM.OE_PIN, GPIO.HIGH)
        GPIO.output(EEPROM.CE_PIN, GPIO.HIGH)

        sleep(EEPROM.OUTPUT_DISABLE_DELAY)

        return byte

    def check_byte(self, address: int, byte: int) -> bool:
        read_byte = self.read_byte(address)
        logger.debug(f'read byte {byte:08b} from address {address:011b}')
        if read_byte != byte:
            logger.warning(f'read value {read_byte:08b} from address {address:011b}, expected {byte:08b}')
            return False
        return True

    def write_byte(self, address: int, byte: int):
        self.set_address(address)

        GPIO.output(EEPROM.OE_PIN, GPIO.HIGH)
        GPIO.output(EEPROM.CE_PIN, GPIO.LOW)

        self.set_gpio_data_pins_to_write()
        self.set_data(byte)

        sleep(EEPROM.ADDRESS_TO_WE_PULSE_START_DELAY)

        GPIO.output(EEPROM.WE_PIN, GPIO.LOW)
        GPIO.output(EEPROM.WE_PIN, GPIO.HIGH)

        GPIO.output(EEPROM.CE_PIN, GPIO.HIGH)

        sleep(EEPROM.WRITE_CYCLE_DELAY)

    def read_bytes(self, addresses: Iterable[int]):
        data = {}
        for address in addresses:
            data[address] = self.read_byte(address)
        return data

    def check_bytes(self, data: dict[int, int]):
        for address, byte in data.items():
            self.check_byte(address, byte)

    def write_bytes(self, data: dict[int, int]):
        for address, byte in data.items():
            self.write_byte(address, byte)

    def cleanup(self):
        GPIO.cleanup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        if exc_type is None:
            return True
        return False

    @staticmethod
    def bool_to_high_low(value):
        return GPIO.HIGH if value else GPIO.LOW
