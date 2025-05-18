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

HT = 1 << 15  # Halt
MI = 1 << 14  # Memory Address Register In
RI = 1 << 13  # RAM In
RO = 1 << 12  # RAM Out
IO = 1 << 11  # Instruction Register Out
II = 1 << 10  # Instruction Register In
AI = 1 << 9   # A Register In
AO = 1 << 8   # A Register Out
EO = 1 << 7   # Sum Out
SU = 1 << 6   # Subtract
BI = 1 << 5   # B Register In
OI = 1 << 4   # Output Register In
CE = 1 << 3   # Counter Enable
CO = 1 << 2   # Counter Out
J = 1 << 1    # Jump

NOP = 0b0000 << 7  # No Operation
LDA = 0b0001 << 7  # Load A
STA = 0b0010 << 7  # Store A
ADD = 0b0011 << 7  #
SUB = 0b0100 << 7
JMP = 0b0101 << 7
LIA = 0b0110 << 7
LIB = 0b0111 << 7
OUT = 0b1110 << 7
HLT = 0b1111 << 7

ALL_INSTRUCTIONS = Options(NOP, LDA, STA, ADD, SUB, JMP, LIA, OUT, HLT)
# 
# NO_FLAGS = 0b0000
# CARRY_FLAG = 0b0001
# ANY_CARRY_FLAG = Options(NO_FLAGS, CARRY_FLAG)
# ZERO_FLAG = 0b0010
# ANY_ZERO_FLAG = Options(NO_FLAGS, ZERO_FLAG)
# ANY_FLAGS = ANY_CARRY_FLAG | ANY_ZERO_FLAG

MICROCODE = {
    ALL_INSTRUCTIONS | STEP_0: MI | CO,
    ALL_INSTRUCTIONS | STEP_1: RO | II | CE,
    Options(LDA, STA, ADD, SUB) | STEP_2: IO | MI,
    LDA | STEP_3: RO | AI,
    STA | STEP_3: AO | RI,
    Options(ADD, SUB) | STEP_3: RO | BI,
    ADD | STEP_4: AI | EO,
    SUB | STEP_4: AI | EO | SU,
    JMP | STEP_2: IO | J,
    LIA | STEP_2: IO | AI,
    LIB | STEP_2: IO | BI,
    OUT | STEP_2: AO | OI,
    HLT | STEP_2: HT,

}

print(Options.expand(MICROCODE))
