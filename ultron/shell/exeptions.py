from typing import Any, Dict, List
from ultron.logger.log import Logger
from ultron.shell.namespaces import UltronCommandsNameSpase
from ultron.utils.enums import CommandLineTypes, EmojiEnum
from ultron.utils.example_shell_code import add_command_help, flag_function_help


class ArgumentError(Exception):
    """An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(self, argument, message):
        self.argument_name = argument
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = "%(message)s"
        else:
            format = "argument %(argument_name)s: %(message)s"
        return format % dict(message=self.message, argument_name=self.argument_name)


class CommandLenError(Exception):
    """An error from creating or using an command.

    The string value of this exception is the message, commented with
    information about the command that caused it.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "You have to pass just"


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
    def command_must_be_at_the_beginning():
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message="command must be at the beginning.",
            color="doc",
            end="\n",
        )
    
    @staticmethod
    def too_much_commands(argv: List):
        print("Command Error Incoming args: ", argv)
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message="command must be at the beginning.",
            color="doc",
            end="\n",
        )

    @staticmethod
    def unknown_argument(argument: str, command: str):
        Logger.header(message="Excution Error", color="error", emoji="error")
        argument = Logger.hint(message=f"--{argument}", color="header")
        command = Logger.hint(message=command, color="header")
        help_hint: Any = Logger.hint(
            f"ultron {command} [-h, --help]", "warning"
        )
        hint_message: str = (
            f"{EmojiEnum.header.value}Try run {help_hint} to get more help."
        )
        return Logger.log(
            message=f"Unknown argument {argument} inside command {command}.\n{hint_message}",
            color="doc",
            end="\n",
        )

    @staticmethod
    def is_required(
        command: str, name: str, type: str = CommandLineTypes.argument.value
    ):
        """
        Return an exception if the command passed without any required arguments of flags.
        command: UltronCommand
        type => CommandLineTypes
        """
        if type == CommandLineTypes.argument.value:
            name = f"--{name}"
        if type == CommandLineTypes.flag.value:
            name = f"-{name}"

        _command: Any = Logger.hint(command)
        _argument: Any = Logger.hint(name)
        help_hint: Any = Logger.hint(f"ultron {command} [-h, --help]", "warning")
        hint_message: str = (
            f"{EmojiEnum.header.value}Try run {help_hint} to get more help."
        )
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"{type} {_argument} of command {_command} is required.\n{hint_message}",
            color="white",
            end="\n",
        )

    @staticmethod
    def flag_not_found(command: str, flag: str):
        help_hint: Any = Logger.hint(f"ultron {command} [-h, --help]", "warning")
        command: Any = Logger.hint(command)
        flag: Any = Logger.hint(f"-{flag}")
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"flag {flag} not found inside command {command}.\n{EmojiEnum.header.value}Try run {help_hint} to get more help.",
            color="doc",
            end="\n",
        )

    @staticmethod
    def missing_argument_format(argument: str, command_name: str):
        foo: Any = Logger.hint("foo")
        if not command_name.startswith("-"):
            help_hint: Any = Logger.hint(
                f"ultron {command_name} {argument} [-h, --help]", "warning"
            )
        else:
            help_hint: Any = Logger.hint("ultron [-h, --help]", "warning")

        argument: Any = Logger.hint(argument)
        Logger.header(message="Excution Error", color="error", emoji="error")
        return Logger.log(
            message=f"Cannot pass arguments without its values, e.g. {argument}={foo}\n Try to run {help_hint}",
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
        if str(wrong_word).startswith("-"):
            print(command)
            wrong_word: str = Logger.hint(wrong_word)
            Logger.header(message="Excution Error", color="error", emoji="error")
            print(wrong_word, right_word, type_, command)
            return
        elif command and type_ == CommandLineTypes.argument.value:
            wrong_word: str = Logger.hint(wrong_word)
            Logger.header(message="Excution Error", color="error", emoji="error")
            help_hint: Any = Logger.hint(f"ultron {command} {right_word}", "warning")
            return Logger.log(
                message=f"""{type_.title()} {wrong_word} not found inside {Logger.hint(command)} command, """.strip()
                + f"""
                did you mean {Logger.hint(right_word)}?\n{EmojiEnum.header.value}Try run {help_hint}
                """.strip(),
                color="doc",
                end="\n",
            )
        else:
            wrong_word: str = Logger.hint(wrong_word)
            Logger.header(message="Excution Error", color="error", emoji="error")
            help_hint: Any = Logger.hint(f"ultron {right_word}", "warning")
            return Logger.log(
                message=f"""
                {type_.title()} {wrong_word} not found,
                """.strip()
                + " "
                + f"""
                did you mean {Logger.hint(right_word)}?\n{EmojiEnum.header.value}Try run '{help_hint}'
                """.strip(),
                color="doc",
                end="\n",
            )

    @staticmethod
    def entry_point_help(commands: Dict[str, UltronCommandsNameSpase]) -> Logger:
        """
        This function prints the entry point of ultron shell,
        that will print all the commands, arguments with its help, required.
        """
        max_len = 0
        Logger.header(
            message="Exctuation Help Command", color="success", emoji="success"
        )
        if len(commands) > 0:
            Logger.log(
                message="The following report contains all defined commands and its attributes.",
                color="doc",
                end="\n\n",
            )
            Logger.log(
                message="Usage: ",
                color="white",
                end="\n",
            )
            Logger.log(
                message=f"\t Commands: {[command_name for command_name, command_values in commands.items()]}",
                color="white",
                end="\n\n",
            )

            for command_name, command_value in commands.items():
                if len(command_name) > max_len:
                    max_len = len(command_name)
                elif len(command_name) > max_len:
                    max_len = len(command_name)

            for command_name, command_value in commands.items():
                _command: Any = Logger.hint(command_name, color="blue")
                command_help: Any = Logger.hint(command_value.help, color="white")
                Logger.log(
                    message="\t\t"
                    + _command
                    + " " * (max_len - len(command_name) + 10)
                    + command_help,
                    color="doc",
                    end="\n",
                )
            Logger.log(message="", color="white", end="\n\t")

            Logger.log(
                message="Actions:",
                color="white",
                end="\n\n",
            )
            Logger.log(
                message=f"\t\t{[command_values.function.__name__ for command_name, command_values in commands.items()]}",
                color="warning",
                end="\n\n",
            )

            Logger.log(
                message="See also there are flags contains various attributes.",
                color="doc",
                end="\n\n",
            )
            flag_funcs: List[str] = []
            for command_name, command_values in commands.items():
                _command_name: Any = Logger.hint(f"{command_name}", color="blue")
                Logger.log(
                    message=f"\t Command: {_command_name}",
                    color="doc",
                    end="\n\n\t",
                )
                if command_values.flags is not None:
                    Logger.log(
                        message=f"\t Flags: {list(command_values.flags.keys())}",
                        color="white",
                        end="\n\n\t",
                    )
                    for flag_name, flag_value in command_values.flags.items():
                        _flag: Any = Logger.hint(f"-{flag_name}")
                        is_required: Any = Logger.hint(
                            flag_value.required, color="blue"
                        )
                        flag_help: Any = Logger.hint(flag_value.help, color="white")
                        Logger.log(
                            message="\t\t"
                            + _flag
                            + " " * (max_len - len(flag_name) + 10)
                            + flag_help
                            + " " * (max_len - len(flag_value.help) + 10)
                            + " Required => "
                            + str(is_required),
                            color="doc",
                            end="\n\t",
                        )
                        flag_funcs.append(flag_value.function.__name__)
                    Logger.log(message="", color="white", end="\n\t\t")
                    Logger.log(
                        message="Actions:",
                        color="white",
                        end="\n\n\t\t",
                    )

                    Logger.log(
                        message=f"\t{flag_funcs}",
                        color="warning",
                        end="\n\n",
                    )
                if command_values.arguments is not None:
                    Logger.log(
                        message=f"\t\t Arguments: {list(command_values.arguments.keys())}",
                        color="white",
                        end="\n\n\t",
                    )
                    for (
                        argument_name,
                        argument_value,
                    ) in command_values.arguments.items():
                        is_required: Any = Logger.hint(
                            argument_value.required, color="blue"
                        )
                        _argument: Any = Logger.hint(f"--{argument_name}")
                        argument_help: Any = Logger.hint(
                            argument_value.help, color="white"
                        )
                        Logger.log(
                            message="\t\t"
                            + _argument
                            + " " * (max_len - len(argument_name) + 10)
                            + argument_help
                            + " " * (max_len - len(argument_value.help) + 10)
                            + " Required => "
                            + str(is_required),
                            color="doc",
                            end="\n",
                        )
        else:
            Logger.log(
                message="There are no commands to generate a help report, register commands by accessing the ultron parser instance.",
                color="white",
                end="\n\n",
            )
            Logger.log(message="e.g.", color="header", end="\n\t")
            add_command_help(
                name="init",
                function="init_project",
                args="<Project name>",
                help="This is a help message.",
            )
            flag_function_help(
                command_name="init",
                flag_name="f",
                function="remove_any_project_with_same_name",
                args="<Project name>",
                help="Remove any project with same name",
            )
