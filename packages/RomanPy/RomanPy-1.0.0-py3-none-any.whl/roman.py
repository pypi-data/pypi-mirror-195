"""
Definition of the RomanPy module.
"""

_ENCODING_ASCII = "ascii"
_ENCODING_UNICODE = "unicode"

_ROMAN_NUMERALS = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I"
}

_ROMAN_MAPPING_UNICODE_UPPER = {
    "IX": "Ⅸ",
    "IV": "Ⅳ",
    "XII": "Ⅻ",
    "XI": "Ⅺ",
    "VIII": "Ⅷ",
    "VII": "Ⅶ",
    "VI": "Ⅵ",
    "III": "Ⅲ",
    "II": "Ⅱ",
    "M": "Ⅿ",
    "D": "Ⅾ",
    "C": "Ⅽ",
    "L": "Ⅼ",
    "X": "Ⅹ",
    "V": "Ⅴ",
    "I": "Ⅰ"
}

_ROMAN_MAPPING_UNICODE_LOWER = {
    "IX": "ⅸ",
    "IV": "ⅳ",
    "XII": "ⅻ",
    "XI": "ⅺ",
    "VIII": "ⅷ",
    "VII": "ⅶ",
    "VI": "ⅵ",
    "III": "ⅲ",
    "II": "ⅱ",
    "M": "ⅿ",
    "D": "ⅾ",
    "C": "ⅽ",
    "L": "ⅼ",
    "X": "ⅹ",
    "V": "ⅴ",
    "I": "ⅰ"
}


class _RomanNumeral:
    """
    The roman numeral class.
    """

    def __init__(self, value: int, **kwargs):
        assert value > 0, "a roman numeral cannot have a value smaller or " \
                          "equal to zero"

        self._value = value

        self._encoding = kwargs.pop("encoding", _ENCODING_ASCII)
        self._uppercase = kwargs.pop("uppercase", True)

        assert self._encoding in (_ENCODING_ASCII, _ENCODING_UNICODE), \
            f"specified encoding \"{self._encoding}\" unknown"

    def encode(self, encoding: str):
        """
        Return a roman numeral of the same value and case as the current
        roman numeral, with the specified encoding.
        """
        return _RomanNumeral(self._value,
                             encoding=encoding,
                             uppercase=self._uppercase)

    def upper(self):
        """
        Return a roman numeral of the same value and encoding as the current
        roman numeral, in uppercase.
        """
        return _RomanNumeral(self._value,
                             encoding=self._encoding,
                             uppercase=True)

    def lower(self):
        """
        Return a roman numeral of the same value and encoding as the current
        roman numeral, in lowercase.
        """
        return _RomanNumeral(self._value,
                             encoding=self._encoding,
                             uppercase=False)

    def __str__(self):
        carry = self._value
        numeral = ""

        for value, digit in _ROMAN_NUMERALS.items():
            while value <= carry:
                carry = carry - value
                numeral = numeral + digit

        if self._encoding is _ENCODING_ASCII:
            return numeral if self._uppercase else numeral.lower()

        mapping = _ROMAN_MAPPING_UNICODE_UPPER if self._uppercase else \
            _ROMAN_MAPPING_UNICODE_LOWER

        for old, new in mapping.items():
            numeral = numeral.replace(old, new)

        return numeral

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, _RomanNumeral):
            return self._value == other._value
        if isinstance(other, int):
            return self._value == other
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented

    def __ne__(self, other):
        return not other == self

    def __gt__(self, other):
        if isinstance(other, _RomanNumeral):
            return self._value > other._value
        if isinstance(other, int):
            return self._value > other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, _RomanNumeral):
            return self._value < other._value
        if isinstance(other, int):
            return self._value < other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, _RomanNumeral):
            return self._value >= other._value
        if isinstance(other, int):
            return self._value >= other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, _RomanNumeral):
            return self._value <= other._value
        if isinstance(other, int):
            return self._value <= other
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, _RomanNumeral):
            return _RomanNumeral(self._value + other._value)
        if isinstance(other, int):
            return _RomanNumeral(self._value + other)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, _RomanNumeral):
            return _RomanNumeral(self._value - other._value)
        if isinstance(other, int):
            return _RomanNumeral(self._value - other)
        return NotImplemented

    __rsub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, _RomanNumeral):
            return _RomanNumeral(self._value * other._value)
        if isinstance(other, int):
            return _RomanNumeral(self._value * other)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, _RomanNumeral):
            return _RomanNumeral(int(self._value / other._value))
        if isinstance(other, int):
            return _RomanNumeral(int(self._value / other))
        return NotImplemented

    __rtruediv__ = __truediv__

    def __floordiv__(self, other):
        if isinstance(other, _RomanNumeral):
            return _RomanNumeral(self._value // other._value)
        if isinstance(other, int):
            return _RomanNumeral(self._value // other)
        return NotImplemented

    __rfloordiv__ = __floordiv__


# pylint:disable = invalid-name
roman = _RomanNumeral
