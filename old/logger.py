class Logger:
    """Intern logger to log messages, debugging in cmd with custom colors."""
    @staticmethod
    def log(
        color: str, message, message_with_color: str = None, end="\n", imo=None
    ) -> None:
        if hasattr(Colors, color):
            if imo is None and message_with_color:
                print(
                    f"{Colors[color].value[0]}{message_with_color}: {Colors.white.value[0]}"
                    + message
                    + end
                )
            elif message_with_color:
                print(
                    f"{Colors[color].value[1]} {Colors[color].value[0]}{message_with_color}: {Colors.white.value[0]}"
                    + message
                    + end
                )
            else:
                print(
                    f"{Colors[color].value[1]} {Colors[color].value[0]}{message} {Colors.white.value[0]}"
                )
            return
        print(f"{Colors.error.value[1]} Color not found {Colors.white.value[0]}")
        return

    @staticmethod
    def hint(message: str, color: str = None) -> None:
        if color:
            hint = f"{Colors[color].value[0]}{message}{Colors.white.value[0]}"
        else:
            hint = f"{Colors.header.value[0]}{message}{Colors.white.value[0]}"
        return hint
