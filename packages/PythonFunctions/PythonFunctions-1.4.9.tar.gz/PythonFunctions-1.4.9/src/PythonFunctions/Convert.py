import typing

from .Message import Message
# Thanks to Guy_732
# changes letter to number based in the alphabet


def decode(s: str) -> int:
    s = s.lower()
    ref = ord("a") - 1
    v = 0
    exp = 1
    for c in reversed(s):
        v += (ord(c) - ref) * exp
        exp *= 26

    return v


def Location(value: str) -> typing.Tuple:
    """Convert a letter number location into two numbers.

    Args:
        value (str): The letter number value to convert.

    Returns:
        typing.Tuple: The result of the conversion.
    """
    letters = ""
    y = ""

    if len(value) >= 2:
        value = value.lower().strip()

        for v in value:
            if v.isdigit():
                y += v
                continue

            letters += v

        if letters == value:
            return Message.clear(
                "Input must contain at least 1 letter and at least 1 integer."), None

        return decode(letters) - 1, int(y) - 1

    return Message.clear(
        "Input must contain at least 1 letter and at least 1 integer."), None
