from ultron.utils.enums import ColorEnum, EmojiEnum


class Logger:
    """Intern logger to log messages, debugging in cmd with custom colors."""

    @staticmethod
    def log(
        message: str,
        color: str,
        emoji: str = None,
        end: str = "",
        no_message_space: bool = False,
    ) -> "Logger":
        """Print a log message"""
        if Logger.hasattr(ColorEnum, color):
            if emoji and Logger.hasattr(EmojiEnum, emoji):
                message: str = f"{ColorEnum[color].value}{EmojiEnum[emoji].value}{message}{ColorEnum.white.value}"
            else:
                if no_message_space:
                    message: str = (
                        f"{ColorEnum[color].value}{message}{ColorEnum.white.value}"
                    )
                else:
                    message: str = (
                        f"{ColorEnum[color].value} {message}{ColorEnum.white.value}"
                    )
            print(message, end=end)
            return
        return Logger.hasattr(ColorEnum, color)

    @staticmethod
    def error(header: str, message: str) -> "Logger":
        """Error method to log error message with red header"""
        print(
            f"{ColorEnum.error.value}{EmojiEnum.error.value}{header}{ColorEnum.white.value}: ",
            end="",
        )
        print(message)
        return

    @staticmethod
    def help(header: str, message: str) -> "Logger":
        """Help method to log help information with yellow header"""
        print(
            f"{ColorEnum.warning.value}{EmojiEnum.warning.value}{header}{ColorEnum.white.value}: ",
            end="",
        )
        print(message)
        return

    @staticmethod
    def hint(message: str, color: str = "header") -> "Logger":
        """Hint method to log a hint message with pink color."""
        return f"{ColorEnum[color].value}{message}{ColorEnum.white.value}"

    @staticmethod
    def header(message: str, color: str, emoji: str = None, end: str = "") -> "Logger":
        """Print a header message"""
        return Logger.log(f"{message}:", color, emoji, end)

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
