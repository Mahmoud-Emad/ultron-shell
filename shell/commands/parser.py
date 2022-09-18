from operator import index
from typing import Any, Dict, List
from shell.errors.handler import ErrorHandler, Handler
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


class UltronCommandLineParser:
    def __init__(self, argv: List):
        self.argv = argv
        self.name_space: Any = Namespace()
        self.help_flags = ["-h", "--help"]

    def parse_args(self):
        command: Any = None
        argument: Any = None
        for keyword in self.argv:
            if keyword in list(self.name_space.commands.keys()):
                command = self.name_space.commands[keyword]
            elif keyword.startswith("--") and keyword not in self.help_flags:
                print(keyword)
            elif keyword in self.help_flags and len(self.argv) <= 1:
                return Handler.entry_point_help(self.name_space.commands)
        print(command)
        # print(self.argv)
        # print(self.name_space.commands)


class UltronCommandLine(UltronCommandLineParser):
    def __init__(self, argv: List):
        UltronCommandLineParser.__init__(self, argv)

    def add_command(self, command: str, help: str) -> Dict[str, Dict]:
        """
        Add a command to the commands,
        `command: command name`,
        `help: help string for the command`.
        """
        if not hasattr(self.name_space, "commands"):
            self.name_space.commands = dict()
        self.name_space.commands[command] = dict(
            name=command,
            help=help,
            args=dict(),
            type=CommandLineTypes.command.value,
        )

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
        `command`: `command name`,
        `argument`: `argument name`,
        `help`: `argument help`,
        `required`: `is this argument is required to excute the command`,
        """
        if not argument.startswith("--"):
            argument = f"--{argument}"

        command["args"][argument] = dict(
            name=argument,
            help=help,
            required=required,
            value=None,
            type=CommandLineTypes.argument.value,
        )
        return command["args"][argument]

    def get_command(self, command: str) -> Dict[str, Dict]:
        """
        Function to get command values [args, helps, required args],
        `command`: instance of command, e.g.
            `ultron: UltronCommandLine = UltronCommandLine()`\n
            `command: Any = ultron.new_command('init', help='the initial command')`\n
            `ultron.get_command(command)`
            `
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

        if self.name_space.commands.get(command.get("name")):
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
            return found
        return ErrorHandler.command_not_found(command.get("name"))

    def set_value(self, command: Dict, argument: Dict, vlaue: Any) -> str:
        """
        returns the value of the command argument.
            command: the instance of the command.
            argument: the instance of the argument.
            value: the value of the command argument.
        """
        args: List = list(command["args"].keys())
        if argument.get("name") not in args:
            return ErrorHandler.argument_not_found(command, argument.get("name"))
        argument["value"] = vlaue
        return self.get_value(command, argument)

    def get_value(self, command: Dict, argument: Dict) -> str:
        """
        returns the value of the command argument.
        """
        args: List = list(command["args"].keys())
        if argument.get("name") not in args:
            return ErrorHandler.argument_not_found(command, argument.get("name"))
        return argument.get("value")

    def delete(self, passed: Dict) -> str:
        """
        delete command or agument.
        passed: the instance of command or agument to delete
        """
        if passed.get("type") == CommandLineTypes.command.value:
            del self.name_space.commands[passed.get("name")]
        elif passed.get("type") == CommandLineTypes.argument.value:
            commands: Dict = self.name_space.commands
            for command in commands:
                if self.name_space.commands[command]["args"].get(passed.get("name")):
                    del self.name_space.commands[command]["args"][passed.get("name")]
        return Handler.deleted(passed.get("name"))

    def commands(self) -> List[str]:
        """Return list of commands."""
        return list(self.name_space.commands.keys())

    def arguments(self, command: Dict) -> List[str]:
        """
        Return list of command args.
        `command` : the instance of the command
        """
        command: Dict = self.name_space.commands[command.get("name")]
        args: List = list(command.get("args").keys())
        return args
