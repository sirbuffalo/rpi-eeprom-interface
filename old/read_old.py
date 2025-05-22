import RPi.GPIO as GPIO

address_pins: tuple[int] = (4, 17, 27, 22, 10, 9, 11, 5, 14, 15, 24)
data_pins: tuple[int] = (6, 13, 19, 20, 16, 12, 7, 8, 25)

WE_PIN: int = 18
OE_PIN: int = 23
CE_PIN: int = 25

# BCM pin 21 = UNUSED, BCM pin 26 = LED


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in address_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in data_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


GPIO.setup(WE_PIN, GPIO.OUT)
GPIO.output(WE_PIN, GPIO.HIGH)
GPIO.setup(OE_PIN, GPIO.OUT)
GPIO.output(OE_PIN, GPIO.LOW)
GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.LOW)

try:
    while True:
        pass
except KeyboardInterrupt:
    pass