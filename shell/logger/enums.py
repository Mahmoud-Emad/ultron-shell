from enum import Enum


class ColorEnum(Enum):
    success = "\033[92m"
    warning = "\033[93m"
    header = "\033[95m"
    error = "\033[91m"
    white = "\033[0m"
    blue = "\033[94m"
    doc = "\033[1m"


class EmojiEnum(Enum):
    success = "\u2705 "
    warning = "\u26A0\uFE0F "
    header = "\U0001f4a1 "
    error = "\U0001f4a3 "
    white = ""
    blue = ""
    doc = "\u2728 "
