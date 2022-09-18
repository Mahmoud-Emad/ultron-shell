from typing import Any, Dict
from shell.logger.enums import CommandLineTypes, EmojiEnum
from shell.logger.logging import Logger


class ErrorHandler:
    """Handler for error messages handling."""

    @staticmethod
    def command_not_found(command: str):
        command: Any = Logger.hint(command)
        help_hint: Any = Logger.hint("ultron [-h, --help]", "warning")
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"command {command} not found.\n{EmojiEnum.header.value}Try run {help_hint} to get more help.",
            color="doc",
            end="\n",
        )

    @staticmethod
    def argument_not_found(command: Dict, argument: str):
        help_hint: Any = Logger.hint(
            f"ultron {command.get('name')} [-h, --help]", "warning"
        )
        command: Any = Logger.hint(command.get("name"))
        argument: Any = Logger.hint(argument)
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
        Logger.header(message="Excution Error", color="error", emoji="error")
        if type_ == CommandLineTypes.argument.value and command:
            help_hint: Any = Logger.hint(f"ultron {command} {right_word}", "warning")
            return Logger.log(
                message=f"""\
                {type_.title()} {wrong_word} not found inside {Logger.hint(command)} command, 
                """.strip()
                + f"""
                did you mean {Logger.hint(right_word)}?\n{EmojiEnum.header.value}Try run {help_hint}
                """.strip(),
                color="doc",
                end="\n",
            )
        else:
            help_hint: Any = Logger.hint(f"ultron {right_word}", "warning")
            return Logger.log(
                message=f"""
                {type_.title()} {wrong_word} not found,
                """.strip()
                + f"""
                did you mean {Logger.hint(right_word)}?\n{EmojiEnum.header.value}Try run {help_hint}
                """.strip(),
                color="doc",
                end="\n",
            )


class Handler:
    @staticmethod
    def deleted(keyword: str) -> Logger:
        """Pass a keyword and return a Logger of deleted"""
        message: str = "command "
        if keyword.startswith("--"):
            message: str = "argument "
        keyword: Any = Logger.hint(keyword)
        Logger.header(message="Success Deleted", color="success", emoji="success")
        return Logger.log(
            message=message + f"%s deleted!" % keyword,
            color="doc",
            end="\n",
        )

    @staticmethod
    def entry_point_help(commands: Dict):
        """
        This function prints the entry point of ultron shell,
        that will print all the commands, arguments with its help, required.
        """
        max_len = 0
        Logger.header(
            message="Exctuation Help Command", color="success", emoji="success"
        )
        Logger.log(
            message="The following report contains all defined commands.",
            color="doc",
            end="\n\n",
        )
        Logger.header(
            message="Commands", color="warning", end="\n"
        )
        for command in commands:
            for argument in commands[command]['args']:
                if len(command) > max_len:
                    max_len = len(command)
                elif len(argument) > max_len:
                    max_len = len(argument)

        for command in commands:
            _command: Any = Logger.hint(command)
            command_help: Any = Logger.hint(commands[command]["help"], color="doc")
            Logger.log(
                message="\t" + _command + " " * (max_len - len(command) + 10) + f"help = {command_help}",
                color="doc",
                end="\n",
            )
        Logger.header(
            message="Arguments", color="warning", end="\n"
        )

        for command in commands:
            _command: Any = Logger.hint(command)
            for argument in commands[command]['args']:
                _argument: Any = Logger.hint(argument)
                argument_help: Any = Logger.hint(commands[command]['args'][argument]['help'], color="doc")
                Logger.log(
                    message="\t" + _argument + " " * (max_len - len(argument) + 10) + f"help = {argument_help}" + f" <{_command}>",
                    color="doc",
                    end="\n",
                )
