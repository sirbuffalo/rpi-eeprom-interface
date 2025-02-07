from __future__ import annotations


class Options:
    def __init__(self, *args):
        bit_arrays = []
        for option in args:
            match option:
                case int():
                    bit_arrays.append(option)
                case Options():
                    bit_arrays.extend(option.bit_arrays)
                case _:
                    raise TypeError(f'Invalid option: {option}')
        self._bit_arrays = frozenset(bit_arrays)

    def __len__(self):
        return len(self._bit_arrays)

    @property
    def bit_arrays(self):
        return self._bit_arrays

    def __or__(self, other):
        if isinstance(other, int):
            return Options(*[bit_array | other for bit_array in self._bit_arrays])
        elif isinstance(other, Options):
            if len(self._bit_arrays) != len(other.bit_arrays):
                raise ValueError("BitArrayArrays must be of equal length for bitwise OR")
            return Options(*[b1 | b2 for b1, b2 in zip(self._bit_arrays, other.bit_arrays)])
        else:
            return NotImplemented

    def __ror__(self, other):
        return self.__or__(other)

    def __and__(self, other):
        if isinstance(other, int):
            return Options(*[bit_array & other for bit_array in self._bit_arrays])
        elif isinstance(other, Options):
            if len(self._bit_arrays) != len(other.bit_arrays):
                raise ValueError("BitArrayArrays must be of equal length for bitwise AND")
            return Options(*[b1 & b2 for b1, b2 in zip(self._bit_arrays, other.bit_arrays)])
        else:
            return NotImplemented

    def __rand__(self, other):
        return self.__and__(other)

    def __xor__(self, other):
        if isinstance(other, int):
            return Options(*[bit_array ^ other for bit_array in self._bit_arrays])
        elif isinstance(other, Options):
            if len(self._bit_arrays) != len(other.bit_arrays):
                raise ValueError("BitArrayArrays must be of equal length for bitwise XOR")
            return Options(*[b1 ^ b2 for b1, b2 in zip(self._bit_arrays, other.bit_arrays)])
        else:
            return NotImplemented

    def __rxor__(self, other):
        return self.__xor__(other)

    def __invert__(self):
        return Options(*[~bit_array for bit_array in self._bit_arrays])

    def __hash__(self):
        return hash(self._bit_arrays)

    def __str__(self):
        return f'Options({", ".join(map(lambda x: f'0b{x:011b}', self._bit_arrays))})'

    def __repr__(self):
        return str(self)

    @staticmethod
    def expand(microcode: dict[int | Options, int]) -> dict[int, int]:
        expanded_microcode = {}
        for key, value in microcode.items():
            match key:
                case Options():
                    for bit_array in key.bit_arrays:
                        expanded_microcode[bit_array] = value
                case int():
                    expanded_microcode[key] = value
                case _:
                    raise TypeError(f'Invalid key: {key}')
        return expanded_microcode


STEP_0 = 0b000 << 4
STEP_1 = 0b001 << 4
STEP_2 = 0b010 << 4
STEP_3 = 0b011 << 4
STEP_4 = 0b100 << 4
STEP_5 = 0b101 << 4
STEP_6 = 0b110 << 4
STEP_7 = 0b111 << 4

ALL_STEPS = Options(STEP_0, STEP_1, STEP_2, STEP_3, STEP_4, STEP_5, STEP_6, STEP_7)

HLT = 1 << 15
MI = 1 << 14
RI = 1 << 13
RO = 1 << 12
IO = 1 << 11
II = 1 << 10
AI = 1 << 9
AO = 1 << 8
EO = 1 << 7
SU = 1 << 6
BI = 1 << 5
OI = 1 << 4
CE = 1 << 3
CO = 1 << 2
J = 1 << 1

NOP = 0b0000 << 7
LDA = 0b0001 << 7
ADD = 0b0010 << 7
SUB = 0b0011 << 7
STA = 0b0100 << 7
LDI = 0b0101 << 7
JMP = 0b0110 << 7
OUT = 0b1110 << 7
HLT = 0b1111 << 7

ALL_INSTRUCTIONS = Options(NOP, LDA, ADD, SUB, STA, LDI, JMP, OUT, HLT)

MICROCODE = {
    ALL_INSTRUCTIONS | STEP_0: MI | CO,
    ALL_INSTRUCTIONS | STEP_1: RO | II | CE,
    Options(LDA, ADD, SUB, STA) | STEP_2: MI | IO,
    Options(ADD, SUB) | STEP_3: MI | RO,
    LDA | STEP_3: RO | IO,
    ADD | STEP_4: AI | EO,
    SUB | STEP_4: AO | EO | SU,
    STA | STEP_4: RI | AO,
    LDI | STEP_2: IO | AI,
    JMP | STEP_2: IO | J,
    OUT | STEP_2: AO | OI,
    HLT | STEP_2: HLT
}


print(Options.expand(MICROCODE))
