from operator import index
from typing import Any, Dict, List
from shell.errors.handler import ErrorHandler
from shell.logger.enums import CommandLineTypes
from utils.missing_chars import find_argument, find_command


class Namespace:
    """Simple object for storing attributes.
    Implements equality by attribute names and values, and provides a simple
    string representation.
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


class UltronCommandLine:
    def __init__(self):
        self.name_space: Any = Namespace()
        self.help_flags = ["-h", "--help"]

    def add_command(self, command: str, help: str) -> Dict[str, Dict]:
        """
        Add a command to the commands,
        command: command name,
        help: help string for the command.
        """
        if not hasattr(self.name_space, "commands"):
            self.name_space.commands = dict()
        self.name_space.commands[command] = dict(name=command, help=help, args=dict())

        return self.name_space.commands[command]

    def add_argument(
        self,
        command: Namespace,
        argument: str,
        help: str = None,
        required: bool = False,
    ) -> Dict[str, Dict]:
        """
        Add a argument to the command following the pattern `--name_of_argument`,
        command: command name,
        argument: argument name,
        help: argument help,
        required: is this argument is required to excute the command,
        """
        if not argument.startswith("--"):
            argument = f"--{argument}"

        command["args"][argument] = dict(help=help, required=required)
        return command

    def get_command(self, command: str) -> Dict[str, Dict]:
        """
        Function to get command values [args, helps, required args],
        command: command name
        """
        found: bool or Dict[str, Dict] = self.name_space.commands.get(command)
        if not found:
            if find_command(command, self.name_space.commands):
                return ErrorHandler.did_you_men(
                    command,
                    find_command(command, self.name_space.commands),
                    CommandLineTypes.command.value,
                )
            return ErrorHandler.command_not_found(command)
        command = found
        return command

    def get_argument(self, command: str, argument: str) -> Dict[str, Dict]:
        """
        Function to get argument values based on command name [helps, is required],
        command: command name
        argument: argument name
        """
        if not argument.startswith("--"):
            argument = f"--{argument}"
        found: Dict or None = command.get("args").get(argument)
        if not found:
            if find_argument(command, argument):
                return ErrorHandler.did_you_men(
                    argument,
                    find_argument(command, argument),
                    CommandLineTypes.argument.value,
                    command=command.get("name"),
                )
            return ErrorHandler.argument_not_found(command, argument)
