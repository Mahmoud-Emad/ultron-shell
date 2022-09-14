from shell.logger.enums import ColorEnum, EmojiEnum


class Logger:
    """Intern logger to log messages, debugging in cmd with custom colors."""

    @staticmethod
    def hasattr(_class: type, instance: str) -> bool or "Logger":
        """Check if the class has an attribute"""
        if not hasattr(_class, instance):
            return Logger.log(
                message="There is no attribute named {} inside class {}".format(
                    instance, _class
                )
            )
        return True

    def header(message: str, color: str, emoji: str = None, end: str = "") -> "Logger":
        """Print a header message"""
        return Logger.log(f"{message}:", color, emoji, end)

    def hint(message: str, color: str = "header"):
        """Print a hint message"""
        message: str = f"{ColorEnum[color].value}{message}{ColorEnum.white.value}"
        return message

    def log(message: str, color: str, emoji: str = None, end: str = "") -> "Logger":
        """Print a log message"""
        if Logger.hasattr(ColorEnum, color):
            if emoji and Logger.hasattr(EmojiEnum, emoji):
                message: str = f"{ColorEnum[color].value}{EmojiEnum[emoji].value}{message}{ColorEnum.white.value}"
            else:
                message: str = (
                    f"{ColorEnum[color].value} {message}{ColorEnum.white.value}"
                )
            print(message, end=end)
            return
        return Logger.hasattr(ColorEnum, color)
