import logging
from time import sleep, perf_counter_ns

import support_testing_off_pi  # noqa: F401
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


ADDRESS_PINS: tuple[int] = (4, 17, 27, 22, 10, 9, 11, 5, 14, 15, 24)
DATA_PINS: tuple[int] = (6, 13, 19, 20, 16, 12, 7, 8)

WE_PIN: int = 18
OE_PIN: int = 23
CE_PIN: int = 25

LED_PIN: int = 26
# BCM pin 21 = UNUSED

T_READ__ADDRESS_CE_OE_TO_OUTPUT_DELAY         = 0.000000150  # 150ns
T_READ__OUTPUT_DISABLE_DELAY                  = 0.000000050  # 50ns

T_WRITE__ADDRESS_TO_WE_PULSE_START_DELAY      = 0.000000010  # 10ns
T_WRITE__WE_PULSE_WIDTH_MIN                   = 0.000000100  # 100ns
# This is a MAX, and unfortunately too short for time.sleep()
T_WRITE__WE_PULSE_WIDTH_MAX                   = 0.000001     # 1us
# T_WRITE__WE_PULSE_END_TO_DATA_LATCHED_DELAY   = 0.000000010  # 10ns
T_WRITE__WRITE_CYCLE_DELAY                    = 0.001        # 1ms


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
    GPIO.setup(ADDRESS_PINS, GPIO.OUT, initial=GPIO.LOW)

    # default gpio pins to read
    set_gpio_data_pins_to_read()

def cleanup():
    GPIO.cleanup()


def set_gpio_data_pins_to_read(): 
    GPIO.setup(DATA_PINS, GPIO.IN)

def set_gpio_data_pins_to_write():
    GPIO.setup(DATA_PINS, GPIO.OUT)


def set_address(address: int):
    assert isinstance(address, int)
    assert 0 <= address < (1 << 11)

    # data = tuple(map(lambda pin_value: GPIO.HIGH if int(pin_value) else GPIO.LOW, f'{address:011b}'))
    address_pin_values = tuple((GPIO.LOW, GPIO.HIGH)[int(pin_value)] for pin_value in f'{address:011b}')
    logger.debug(f"Setting address pins {ADDRESS_PINS} to {address_pin_values}")

    GPIO.output(ADDRESS_PINS, address_pin_values)

def set_data(data: int):
    # for pin, val in zip(data_pins, f'{data:08b}'):
    #     GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)
    assert isinstance(data, int)
    assert 0 <= data < (1 << 8)

    # data = tuple(map(lambda pin_value: GPIO.HIGH if int(pin_value) else GPIO.LOW, f'{data:08b}'))
    data_pin_values = tuple((GPIO.LOW, GPIO.HIGH)[int(pin_value)] for pin_value in f'{data:08b}')
    logger.debug(f"Setting data pins {DATA_PINS} to {data_pin_values}")

    GPIO.output(DATA_PINS, data_pin_values)

def read_data():
    byte = 0
    for i, pin in enumerate(DATA_PINS):
        if GPIO.input(pin):
            byte |= (1 << i)
    
    assert 0 <= byte < (1 << 8)
    return byte


def read_byte(address: int):
    GPIO.output(WE_PIN, GPIO.HIGH)

    set_address(address)

    set_gpio_data_pins_to_read()
    GPIO.output(CE_PIN, GPIO.LOW)
    GPIO.output(OE_PIN, GPIO.LOW)

    sleep(T_READ__ADDRESS_CE_OE_TO_OUTPUT_DELAY)

    byte = read_data()

    logger.debug(f'read_byte: read value {byte:08b} from address {address:011b}')

    # add a breakpoint on the next line to use a multimeter before disabling chip output
    GPIO.output(OE_PIN, GPIO.HIGH)
    GPIO.output(CE_PIN, GPIO.HIGH)

    # probably overkill given python overhead
    sleep(T_READ__OUTPUT_DISABLE_DELAY)

    return byte


def write_byte(address: int, data: int):
    # assuming setup code set WE to high

    logger.debug(f'write_byte: preparing to write {data:08b} to address {address:011b}')

    set_address(address)
    GPIO.output(OE_PIN, GPIO.HIGH)
    GPIO.output(CE_PIN, GPIO.LOW)
    set_gpio_data_pins_to_write()
    set_data(data)
    sleep(T_WRITE__ADDRESS_TO_WE_PULSE_START_DELAY)
    
    # pulse WE low here, is python too slow to make a pulse < 1 us but the chip doesn't seem to care?
    t0 = perf_counter_ns()
    GPIO.output(WE_PIN, GPIO.LOW)
    t1 = perf_counter_ns()
    GPIO.output(WE_PIN, GPIO.HIGH)
    t2 = perf_counter_ns()

    logger.debug(f'WE timing: output low = {t1 - t0}ns, output high = {t2 - t1}ns. Datasheet wanted < 1000ns ?')
    
    GPIO.output(CE_PIN, GPIO.HIGH)

    sleep(2*T_WRITE__WRITE_CYCLE_DELAY)
