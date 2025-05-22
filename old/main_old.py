from time import sleep
from bitstring import BitArray

import support_testing_off_pi
import RPi.GPIO as GPIO


def set_address(address: int):
    for pin, val in zip(address_pins, f'{address:011b}'):
        GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)

def set_data(data: int):
    for pin, val in zip(data_pins, f'{data:08b}'):
        GPIO.output(pin, GPIO.HIGH if val == '1' else GPIO.LOW)

def write(address: BitArray, data: BitArray):
    set_address(address)
    set_data(data)
    sleep(0.001)
    GPIO.output(WE_PIN, GPIO.LOW)
    sleep(0.001)
    GPIO.output(WE_PIN, GPIO.HIGH)


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


GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.HIGH)
GPIO.setup(OE_PIN, GPIO.OUT)
GPIO.output(OE_PIN, GPIO.HIGH)
GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.LOW)
