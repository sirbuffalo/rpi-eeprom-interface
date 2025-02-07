import RPi.GPIO as GPIO
import time

# --- Pin assignments (using BCM numbering) ---
# Address pins A0-A10
ADDR_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6]

# Data pins D0-D7
DATA_PINS = [14, 15, 18, 23, 24, 25, 8, 7]

# Control pins: /CE, /OE, /WE (active low)
CE_PIN = 13
OE_PIN = 19
WE_PIN = 26

# Write cycle delay (in seconds) - adjust per EEPROM datasheet (typically 5-10ms)
WRITE_DELAY = 0.01

# --- GPIO Setup ---
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up address pins as outputs
    for pin in ADDR_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # For control pins, set as outputs and default them HIGH (inactive)
    for ctrl_pin in [CE_PIN, OE_PIN, WE_PIN]:
        GPIO.setup(ctrl_pin, GPIO.OUT)
        GPIO.output(ctrl_pin, GPIO.HIGH)
    
    # Set up data pins initially as outputs (for write); will reconfigure to input for read
    for pin in DATA_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# --- Helper Functions ---
def set_address(address):
    """
    Set the address lines (A0-A10) to the specified integer (0 - 2047).
    """
    if address < 0 or address > 0x7FF:
        raise ValueError("Address must be between 0 and 2047 (0x7FF)")
    for i, pin in enumerate(ADDR_PINS):
        # Test bit i of the address
        GPIO.output(pin, GPIO.HIGH if (address >> i) & 1 else GPIO.LOW)

def set_data_pins_as_output():
    for pin in DATA_PINS:
        GPIO.setup(pin, GPIO.OUT)

def set_data_pins_as_input():
    for pin in DATA_PINS:
        GPIO.setup(pin, GPIO.IN)

def write_data(value):
    """
    Set the data bus (D0-D7) to the specified 8-bit value.
    """
    if value < 0 or value > 0xFF:
        raise ValueError("Data must be 8-bit (0-255)")
    for i, pin in enumerate(DATA_PINS):
        GPIO.output(pin, GPIO.HIGH if (value >> i) & 1 else GPIO.LOW)

def read_data():
    """
    Read an 8-bit value from the data bus (D0-D7) and return it.
    """
    value = 0
    for i, pin in enumerate(DATA_PINS):
        if GPIO.input(pin):
            value |= (1 << i)
    return value

# --- EEPROM Operations ---
def eeprom_write_byte(address, data):
    """
    Write an 8-bit data byte to the specified address.
    """
    # Set address and data
    set_address(address)
    set_data_pins_as_output()
    write_data(data)
    
    # Activate the chip for writing:
    # /CE low, /OE high (disable output), pulse /WE low
    GPIO.output(CE_PIN, GPIO.LOW)   # Enable chip
    GPIO.output(OE_PIN, GPIO.HIGH)   # Ensure output disabled during write
    time.sleep(0.000001)             # small delay (1 µs)

    GPIO.output(WE_PIN, GPIO.LOW)    # Begin write pulse
    time.sleep(0.000005)             # Pulse width; adjust per datasheet (e.g. 5 µs)
    GPIO.output(WE_PIN, GPIO.HIGH)   # End write pulse

    # Disable chip to complete the cycle
    GPIO.output(CE_PIN, GPIO.HIGH)

    # Wait for the write cycle to complete (typical EEPROM write cycle might be 10ms)
    time.sleep(WRITE_DELAY)

def eeprom_read_byte(address):
    """
    Read an 8-bit data byte from the specified address.
    """
    # Set address
    set_address(address)
    
    # Prepare data bus for reading
    set_data_pins_as_input()
    
    # Activate the chip for reading:
    # /CE and /OE low, /WE high
    GPIO.output(WE_PIN, GPIO.HIGH)   # Ensure write is disabled
    GPIO.output(CE_PIN, GPIO.LOW)
    GPIO.output(OE_PIN, GPIO.LOW)
    
    time.sleep(0.000001)  # Small settling delay (1 µs)
    
    value = read_data()

    # Deactivate the chip (return to idle _state)
    GPIO.output(CE_PIN, GPIO.HIGH)
    GPIO.output(OE_PIN, GPIO.HIGH)
    
    # Optionally, set data pins back to output (depends on your application)
    set_data_pins_as_output()
    
    return value


# --- Main Program ---
if __name__ == "__main__":
    try:
        setup()
        print("EEPROM Interface Ready.")
        
        # Example: Write the byte 0xAB to address 0x123, then read it back
        test_address = 0x123  # Example address (291 decimal)
        test_data = 0xAB      # Example data (171 decimal)
        
        print(f"Writing 0x{test_data:02X} to address 0x{test_address:03X}...")
        eeprom_write_byte(test_address, test_data)
        print("Write complete.")
        
        print(f"Reading from address 0x{test_address:03X}...")
        read_val = eeprom_read_byte(test_address)
        print(f"Data read: 0x{read_val:02X}")
        
    except Exception as e:
        print("Error:", e)
    finally:
        GPIO.cleanup()
