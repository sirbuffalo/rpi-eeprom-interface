import RPi.GPIO as GPIO
import time

# Set the GPIO pin number (BCM numbering) to which your LED is connected
LED_PIN = 18

def main():
    # Use BCM numbering for the GPIO pins
    GPIO.setmode(GPIO.BCM)
    # Set up the LED_PIN as an output
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    try:
        print("Blinking LED on GPIO18. Press Ctrl+C to exit.")
        while True:
            # Turn LED ON
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(1)  # LED stays on for 1 second
            # Turn LED OFF
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(1)  # LED stays off for 1 second
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        # Clean up GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    main()
