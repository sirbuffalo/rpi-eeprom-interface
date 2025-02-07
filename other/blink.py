import RPi.GPIO as GPIO
import time


# Set the GPIO pin number (BCM numbering) to which your LED is connected
LED_PIN = 18


def main():
    GPIO.setmode(GPIO.BCM)

    # Set up the LED_PIN as an output
    GPIO.setup(LED_PIN, GPIO.OUT)

    try:
        print("Blinking LED on GPIO18. Press Ctrl+C to exit.")

        while True:
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        # Clean up GPIO settings
        GPIO.cleanup()


if __name__ == "__main__":
    main()
