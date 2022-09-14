from typing import Dict
from shell.logger.enums import CommandLineTypes, EmojiEnum
from shell.logger.logging import Logger


class ErrorHandler:
    """Handler for error messages handling."""

    @staticmethod
    def command_not_found(command: str):
        command: str = Logger.hint(command)
        help_hint: str = Logger.hint("ultron [-h, --help]", "warning")
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"command {command} not found.\n{EmojiEnum.header.value}Try run {help_hint} to get more help.",
            color="doc",
            end="\n",
        )

    @staticmethod
    def argument_not_found(command: Dict, argument: str):
        help_hint: str = Logger.hint(
            f"ultron {command.get('name')} [-h, --help]", "warning"
        )
        command: str = Logger.hint(command.get("name"))
        argument: str = Logger.hint(argument)
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"argument {argument} not found inside command {command}.\n{EmojiEnum.header.value}Try run {help_hint} to get more help.",
            color="doc",
            end="\n",
        )

    @staticmethod
    def did_you_men(
        wrong_word: str,
        right_word: str,
        type_: str = CommandLineTypes.command.value,
        command: None = None,
    ):
        """
        Handler method returns hint to any matched keyword.
        wrong_word: wrong word typed by user -command -argument
        right_word: the actual right word -command -argument
        type: type -command -argument.
        """
        wrong_word: str = Logger.hint(wrong_word)
        right_word: str = Logger.hint(right_word)
        Logger.header(message="Excution Error", color="error", emoji="error")
        if type_ == CommandLineTypes.argument.value and command:
            command: str = Logger.hint(command)
            help_hint: str = Logger.hint(f"ultron {command} {right_word}", "warning")
            return Logger.log(
                message=f"{type_.title()} {wrong_word} not found inside {command} command, did you mean {right_word}?\n{EmojiEnum.header.value}Try run {help_hint}",
                color="doc",
                end="\n",
            )
        else:
            help_hint: str = Logger.hint(f"ultron {right_word}", "warning")
            return Logger.log(
                message=f"{type_.title()} {wrong_word} not found, did you mean {right_word}?\n{EmojiEnum.header.value}Try run {help_hint}",
                color="doc",
                end="\n",
            )
