import RPi.GPIO as GPIO
from bitstring import BitArray
from time import sleep

def set_address(address: BitArray):
    for pin, val in zip(address_pins, address):
        GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)

def set_data(data: BitArray):
    for pin, val in zip(data_pins, data):
        GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)

def write(address: BitArray, data: BitArray):
    set_address(address)
    set_data(data)
    sleep(0.001)
    GPIO.output(WE_PIN, GPIO.LOW)
    sleep(0.001)
    GPIO.output(WE_PIN, GPIO.HIGH)


address_pins: tuple[int] = (4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19)
data_pins: tuple[int] = (14, 15, 18, 23, 24, 25, 8, 7)
CE_PIN: int = 16
OE_PIN: int = 20
WE_PIN: int = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in address_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in data_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.HIGH)
GPIO.setup(OE_PIN, GPIO.OUT)
GPIO.output(OE_PIN, GPIO.HIGH)
GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.LOW)
