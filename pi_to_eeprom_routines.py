import logging
from time import sleep

import support_testing_off_pi
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


address_pins: tuple[int] = (4, 17, 27, 22, 10, 9, 11, 5, 14, 15, 24)
data_pins: tuple[int] = (6, 13, 19, 20, 16, 12, 7, 8)

WE_PIN: int = 18
OE_PIN: int = 23
CE_PIN: int = 25

LED_PIN: int = 26

# BCM pin 21 = UNUSED


def initialize_led_pin():
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

def enable_led():
    GPIO.output(LED_PIN, GPIO.HIGH)

def disable_led():
    GPIO.output(LED_PIN, GPIO.LOW)


def initialize_pins_and_disable_chip():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    initialize_led_pin()

    # set default state to chip disabled
    GPIO.setup(WE_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(OE_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(CE_PIN, GPIO.OUT, initial=GPIO.HIGH)

    # default address is 0x000
    GPIO.setup(address_pins, GPIO.OUT, initial=GPIO.LOW)

    # default gpio pins to read
    set_gpio_pin_to_read()

def cleanup():
    GPIO.cleanup()


def set_gpio_pin_to_read():
    GPIO.setup(data_pins, GPIO.IN)

def set_gpio_pin_to_write():
    GPIO.setup(data_pins, GPIO.OUT)


def read():
    set_gpio_pin_to_read()

    GPIO.output(WE_PIN, GPIO.HIGH)   # could convert this to a check?
    GPIO.output(CE_PIN, GPIO.LOW)
    GPIO.output(OE_PIN, GPIO.LOW)



def set_address(address: int):
    assert isinstance(address, int)
    assert 0 <= address < 1 << 11

    data = tuple(map(lambda x: GPIO.HIGH if int(x) else GPIO.LOW, f'{address:011b}'))
    logger.debug(f"Setting address {address_pins} to {data}")

    GPIO.output(address_pins, data)


def set_data(data: int):
    # for pin, val in zip(data_pins, f'{data:08b}'):
    #     GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)
    pass


def write(address: int, data: int):
    set_address(address)
    # set_data(data)
    # sleep(0.001)
    # GPIO.output(WE_PIN, GPIO.LOW)
    # sleep(0.001)
    # GPIO.output(WE_PIN, GPIO.HIGH)
