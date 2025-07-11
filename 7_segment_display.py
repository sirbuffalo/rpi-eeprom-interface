from eeprom import EEPROM
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)
logger = logging.getLogger(__name__)

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
    print(number)
    char_num = (address & 0b00000000110) >> 1
    print(char_num)
    if address & 0b00000000001:
        number = int.from_bytes((0b11111101).to_bytes(), signed=True)
    digit = str(number).rjust(4)[char_num]
    return seven_segment_display[digit]

print(get_value(0b0110))
# data = {}
# for x in range(2 ** 11):
#     data[x] = get_value(x)
# print(data)
# logger.debug('\n'.join([f'{address:011b}: {byte:08b}' for address, byte in data.items()]))

# with EEPROM() as eeprom:
#     eeprom.write_bytes(data)
#     eeprom.check_bytes(data)
