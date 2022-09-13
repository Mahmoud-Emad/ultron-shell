from typing import Any, Dict
from shell.errors.handler import ErrorHandler




class Namespace():
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
        # Logger.log(message = "Excuted:", color="success", emoji="success")
        # Logger.log(message = "command init", color="docs", end="\n")

    def add_command(self, command: str, help: str) -> Dict[str, Dict]:
        """
        Add a command to the commands,
        command: command name,
        help: help string for the command.
        """
        self.name_space.commands = dict()
        self.name_space.commands[command] = dict(
            name = command, help = help, args = dict()
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
            return ErrorHandler.command_not_found(command)
        command = found    
        return command

    def get_argument(self, command: str, argument: str) -> Dict[str, Dict]:
        """
        Function to get argument values based on command name [helps, is required],
        command: command name
        argument: argument name
        """
        args: Dict = command.get('args')
        if not argument.startswith("--"):
        #     # TODO: Error handling.
            argument = f"--{argument}"
        argument: Dict[str, Dict] = command.get("args").get(argument)
        return argument
