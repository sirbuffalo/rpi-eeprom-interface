from gpiozero import LED
from time import sleep


# Set the GPIO pin number (BCM numbering) to which your LED is connected
LED_PIN = 18

def main():
    red = LED(LED_PIN)

    while True:
        red.on()
        sleep(1)
        red.off()
        sleep(1)


if __name__ == "__main__":
    main()
