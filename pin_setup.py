import logging
from time import sleep

from gpiozero import LED, Button
from gpiozero.pins.mock import MockPin

logging.basicConfig(level=logging.DEBUG)


try:
    raise ImportError("testing mocked GPIO")

    from gpiozero.pins.rpigpio import RPiGPIOFactory

    factory = RPiGPIOFactory()
    logging.info("Running with real GPIO access.")
    gpio_available = True
except ImportError:
    from gpiozero.pins.mock import MockFactory

    factory = MockFactory(revision="d04170", pin_class=MockPin)
    logging.info("RPi GPIO pin library unavailable, using a Mock PinFactory.")
    gpio_available = False


test_led = LED(21, pin_factory=factory)


while True:
    test_led.on()
    sleep(1)
    test_led.off()
    sleep(1)
