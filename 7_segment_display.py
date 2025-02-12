from eeprom import EEPROM

seven_segment_display = {
    ' ': 0b00000000,
    '-': 0b00000010,
    '0': 0b11111100,
    '1': 0b01100000,
    '2': 0b11011010,
    '3': 0b11110010,
    '4': 0b01100110,
    '5': 0b10110110,
    '6': 0b10111110,
    '7': 0b11100000,
    '8': 0b11111110,
    '9': 0b11110110
}

def get_value(address):
    number = (address & 0b11111111000) >> 3
    char_num = (address & 0b00000000110) >> 1
    if address & 0b00000000001:
        number = int.from_bytes((0b11111101).to_bytes(), signed=True)
    digit = str(number).rjust(4)[char_num]
    return seven_segment_display[digit]


data = {}
for x in range(2 ** 11):
    data[x] = get_value(x)

with EEPROM() as eeprom:
    eeprom.write_bytes(data)
    eeprom.check_bytes(data)
