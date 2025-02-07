class Condition:
    def __init__(self, **args):
        pass

    class MultiPart:
        def __init__(self, *args):
            parts = set()
            for arg in args:
                match arg:
                    case Condition.Part():
                        parts.add(arg)
                    case Condition.MultiPart():
                        parts.update(arg.parts)
                    case _:
                        raise ValueError(f'Invalid part: {arg}')
            self._parts = frozenset(parts)

        @property
        def parts(self):
            return self._parts

        def __len__(self):
            return len(self._parts)

        def _do_op(self, other, op):
            match other:
                case Condition.Part():
                    return Condition.MultiPart(map(lambda part: op(part, other), self._parts))
                case Condition.MultiPart():
                    return Condition.MultiPart(map(lambda other_part: self._do_op(other_part, op), other))
                case _:
                    return NotImplemented

        def __iter__(self):
            return iter(self._parts)

        def __str__(self):
            return ' | '.join(map(str, self._parts))

        def __hash__(self):
            return hash(self._parts)


    class Part:
        def __init__(self, value, length):
            self._value = value
            self._length = length

        @property
        def value(self):
            return self._value

        def __len__(self):
            return self._length

        def __str__(self):
            return f'{self._value:0{self._length}b}'

        def _do_op(self, other, op):
            match other:
                case Condition.Part():
                    return op(self, other)
                case Condition.MultiPart():
                    return Condition.MultiPart(*map(lambda part: op(self, part), other.parts))
                case _:
                    return NotImplemented

        def __or__(self, other):
            return self._do_op(other, lambda a, b: Condition.Part(a.value | b.value, max(a._length, len(b))))

        def __and__(self, other):
            return self._do_op(other, lambda a, b: Condition.Part(a.value & b.value, max(a._length, len(b))))

        def __xor__(self, other):
            return self._do_op(other, lambda a, b: Condition.Part(a.value ^ b.value, max(a._length, len(b))))

        def __not__(self):
            return Condition.Part(~self._value, self._length)

        def __eq__(self, other):
            if isinstance(other, Condition.Part):
                return self._value == other._value and self._length == other._length
            else:
                return NotImplemented

        def __hash__(self):
            return hash((self._value, self._length))

STEP_0 = Condition.Part(0b00000000000, 11)
STEP_1 = Condition.Part(0b00100000000, 11)
STEP_2 = Condition.Part(0b01000000000, 11)
STEP_3 = Condition.Part(0b01100000000, 11)
STEP_4 = Condition.Part(0b10000000000, 11)
STEP_5 = Condition.Part(0b10100000000, 11)
STEP_6 = Condition.Part(0b11000000000, 11)
STEP_7 = Condition.Part(0b11100000000, 11)
STEPS = Condition.MultiPart(STEP_1, STEP_2, STEP_3, STEP_4, STEP_5, STEP_6, STEP_7)

print(STEPS)