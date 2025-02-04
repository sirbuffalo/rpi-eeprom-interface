import logging

from gpiozero import DigitalOutputDevice, DigitalInputDevice, LED
from gpiozero.pins.mock import MockPin, MockFactory

logger = logging.getLogger(__name__)


# Custom pin that logs the result of _change_state
class LoggingMockPin(MockPin):
    def _change_state(self, value):
        result = super()._change_state(value)
        if result:
            logger.debug("LoggingMockPin %s: _change_state(%s) returned True (state changed).", self, value)
        else:
            logger.debug("LoggingMockPin %s: _change_state(%s) returned False (no change).", self, value)
        return result


try:
    # raise ImportError("testing mocked GPIO")

    from gpiozero.pins.rpigpio import RPiGPIOFactory

    factory = RPiGPIOFactory()
    logger.info("Running with real GPIO access.")
    gpio_available = True

except ImportError:
    factory = MockFactory(revision="d04170", pin_class=LoggingMockPin)
    logger.info("RPi GPIO pin library unavailable, using a Mock PinFactory.")
    gpio_available = False

# note: are we going to be closing all these input and output devices each time we switch from reading to writing?
# maybe better to use lower level pin access, like RPi.GPIO .OUT and .IN configuration?
data_pins = [DigitalOutputDevice(pin, initial_value=False, pin_factory=factory) for pin in [4, 17, 27, 22, 10, 9, 11, 5]]
# data_pins = [DigitalInputDevice(pin, pull_up=None, active_state=True, pin_factory=factory) for pin in [4, 17, 27, 22, 10, 9, 11, 5]]

address_pins = [DigitalOutputDevice(pin, initial_value=False, pin_factory=factory) for pin in [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20]]

# Control pins: /CE, /OE, /WE (active low)
CE_PIN = 6
OE_PIN = 13
WE_PIN = 19

control_pin_ce = DigitalOutputDevice(CE_PIN, active_high=False, initial_value=True, pin_factory=factory)
control_pin_oe = DigitalOutputDevice(OE_PIN, active_high=False, initial_value=True, pin_factory=factory)
control_pin_we = DigitalOutputDevice(WE_PIN, active_high=False, initial_value=True, pin_factory=factory)

LED_TEST_PIN = 21
test_led = LED(21, pin_factory=factory)
