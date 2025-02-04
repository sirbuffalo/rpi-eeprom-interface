from gpiozero import DigitalOutputDevice, LED

from time import sleep


data_pins = [DigitalOutputDevice(pin) for pin in [4, 17, 27, 22, 10, 9, 11, 5]]
address_pins = [DigitalOutputDevice(pin) for pin in [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20]]

LED_TEST_PIN = 21


def set_address(address):
    for pin, value in zip(address_pins, f'{address:011b}'):
        if int(value):
            pin.on()
        else:
            pin.off()

def set_data(data):
    for pin, value in zip(data_pins, f'{data:08b}'):
        if int(value):
            pin.on()
        else:
            pin.off()


def main():
    test_led = LED(21)

    while True:
        test_led.on()
        sleep(1)
        test_led.off()
        sleep(1)


if __name__ == "__main__":
    main()