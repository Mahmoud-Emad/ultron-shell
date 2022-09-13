from shell.errors.handler import ErrorHandler
from shell.logger.enums import ColorEnum, EmojiEnum


class Logger:
    """Intern logger to log messages, debugging in cmd with custom colors."""

    @staticmethod
    def log(message: str, color: str, emoji:str = None, end: str = "\n"):
        if hasattr(ColorEnum, color):
            if emoji:
                message: str = f"{ColorEnum[color].value}{EmojiEnum[emoji].value} {message}{ColorEnum.white.value}"
                print(message, end=end)
                return
            message: str = f"{ColorEnum[color].value}{message}{ColorEnum.white.value}"
            print(message, end=end)
            return
        return ErrorHandler.no_color_found(color)

    @staticmethod
    def error_log(message: str, end: str = "\n"):
        message: str = f"{ColorEnum.error.value}{EmojiEnum.error.value} {message}{ColorEnum.white.value}"
        print(message, end=end)
        return
