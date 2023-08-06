# pylint: disable=W0611
from colorama import Fore, Back, Style
from colorama.ansi import AnsiCodes
# Disabled as imported from other module to make it all fit together
# pylint: enable=W0611


class FORMAT(AnsiCodes):
    RESET = 0
    BOLD = 1
    DISABLE = 2
    ITALIC = 3
    UNDERLINE = 4
    REVERSE = 7
    INVISIBLE = 8
    STRIKETHROUGH = 9
