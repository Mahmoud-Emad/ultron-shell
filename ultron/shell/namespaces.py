import inspect
from typing import List, Optional, Dict, Any, Callable
import random
import base64
import os


class UltronCommandsNameSpase:
    def __init__(self):
        self.commands: Dict = {}
        self.command: Dict = {}
        self.listed_commands: List[str] = []

    def add(self, command: str) -> List[str]:
        if command not in self.commands:
            self.commands[command.name] = command
        return self.commands

    def __str__(self):
        return f"<{self.__class__.__name__} commands={self.commands}>"

    def __from_namespace__(self):
        """Returns all commands in the standered image"""
        return self.commands

    def all(self):
        """Return a list of all commands."""
        return [k for k, _ in self.commands.items()]

    def get(self, command: str) -> "UltronCommand":
        """Get UltronCommand from listed commands."""
        for command_, command_value in self.commands.items():
            if command_ == command:
                return command_value
        return None


class UltronNameSpace:
    def __init__(self):
        self.commands = UltronCommandsNameSpase()
        self.name = None
        self.flags: List[str] = []
        self.list_str_flags: List[str] = []

    def get_list_str_flags(self):
        for _, command_values in self.commands.__from_namespace__().items():
            if command_values.flags is not None:
                for flag in list(command_values.flags.keys()):
                    self.list_str_flags.append(flag)
        return self.list_str_flags

    def list_command_flags(self, command: "UltronCommand", flag_name: str):
        return list(command.flags.keys())

    def add(self, command: "UltronCommand"):
        """
        takes the command and set it inside commands namespace.
            parameters: command => UltronCommandParser
        """
        if self.name is None:
            self.name = self.generate_namespace_name()
        return self.commands.add(command)

    def get(self, command: str) -> UltronCommandsNameSpase:
        """Return command from namespace"""
        return self.commands.get(command)

    def __str__(self):
        return f"<{self.__class__.__name__} name='{self.name}' commands={self.commands.all()}>"

    def generate_namespace_name(self) -> str:
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        self.abspath = os.path.normpath(self.current_path + os.sep + os.pardir)
        self.file_path = os.path.join(f"{self.abspath}/utils/namespace_names.txt")
        if self.name is None:
            file_content: str or None = None
            with open(self.file_path, "r") as f:
                file_content: str = base64.b64decode(f.read())
            if file_content is None:
                raise ValueError("Name cannot generate")
            return "".join(random.choice(str(file_content).split(" ")))
        return self.name


class UltronArgumentParser:
    def __init__(
        self, name: str, help: str, defult: str or None = None, required: bool = False
    ):
        """
        ### Class ultron argument parser.
        #### README `takes the argument name and the action will excuting when the end user pass the command`.
            * name      : type(str) the name of argumrnt.
            * defult    : type(Any) a defult value if the user didn't pass the argument,
                            it can be a list if the command function require more than argument.
            * help      : type(str) a help message will be displayed when the end user pass --help.
            * required  : type(bool) Set it to true when you have to make this argument reuired to excute the command.
        """
        if name.startswith("--"):
            name = name.replace("--", "")

        if help == None:
            help = "--"

        self.name = name
        self.help = help
        self.defult = defult
        self.required = required

    def __str__(self):
        return f"<{self.__class__.__name__} name='{self.name}', value={self.defult}, help='{self.help}', required={self.required}>"

    def get(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{self.__class__.__name__} has no attribute named '{key}'.")

class UltronFlagParser:
    def __init__(
        self,
        name: str,
        function: Callable,
        args: Optional[List[Any]] or str or None = None,
        help: Optional[str] or None = None,
        required: Optional[bool] = False,
    ) -> "UltronFlagParser":
        """
        ### Class ultron flags parser.
        #### README `takes the flag name and the action will excute when the flag passed in the command`.
            * name      : type(str) the name of flag.
            * function  : type(function) a hook function that can excute when the flag passed in the command.
            * args      : type(list) a list of arguments that are required to the hook function.
            * help      : type(str) a help message will be displayed when the end user pass --help.
            * required  : type(bool) Set it to true when you have to make this flag reuired to excute the command.
        """
        if name.startswith("-"):
            name = name.replace("-", "")

        if help == None:
            help = "--"

        self.name = name
        self.function = function
        self.args = args
        self.help = help
        self.required = required

    def __str__(self):
        return f"<{self.__class__.__name__} name='{self.name}', function={self.function.__name__}, args={self.args}, help='{self.help}', required={self.required}>"

    def get(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{self.__class__.__name__} has no attribute named '{key}'.")


class UltronCommandNameSpace:
    def __init__(
        self,
        name: str,
        function: Callable,
        flags: Optional[UltronFlagParser] or UltronFlagParser or None = None,
        arguments: Optional[UltronArgumentParser] or UltronArgumentParser or None = None,
        help: Optional[str] or None = None,
    ):
        self.name = name
        self.flags = flags
        self.function = function
        self.arguments = arguments
        if help is None:
            help = "No help available!"
        self.help = help
        self.required_flag = None

    def __str__(self):
        return f"<UltronCommandNameSpace name={self.name}>"

    def __getattr__(self, attr: str):
        """Get attribute value, attr => name of attribute"""
        if hasattr(self, attr):
            return getattr(self, attr)
        return None

    def has_required_flags(self):
        """A helper method that can check if flag is required or not."""
        if self.flags:
            for _, flag in self.flags.items():
                if flag.required:
                    self.required_flag = flag
                    return True
            return False
        return False

    def get_required_flag(self):
        if self.required_flag is not None:
            return self.required_flag
        for _, flag in self.flags.items():
            if flag.required:
                self.required_flag = flag
        return self.required_flag

    def extract_arguments_and_do_action(self):
        """Return a list of the arguments if the arguments > 1, otherwise return the actual argumen name."""
        listed_args: List[str] = []
        if self.arguments is not None:
            if type(self.arguments) == list:
                for argument in self.arguments:
                    listed_args.append(argument.defult)
                return self.__do_action(*listed_args)
            else:
                return self.__do_action(self.arguments.defult)
        return self.__do_action()

    def __do_action(self, *args: List[str] or UltronArgumentParser):
        """Call the command action function"""
        return self.function(*args)
    
    def listed_arguments_names(self):
        """Return a list of str of arguements names"""
        args: List[str] = []
        if type(self.arguments) == list:
            for arg in self.arguments:
                args.append(arg.name)
            return args
        args.append(self.arguments.name)
        return args

    def register_arguments(self, arguments: List[Dict]):
        """Loop over incoming arguments and register it on the command."""
        function_args: List(str) = inspect.getfullargspec(self.function).args
        for argument in arguments:
            for arg_name, arg_value in argument.items():
                if arg_name not in function_args or arg_name not in self.listed_arguments_names():
                    return (False, arg_name)
                
                if type(self.arguments) == list:
                    for argument in self.arguments:
                        if argument.name == argument:
                            argument.defult = arg_value
                            return self.arguments
                self.arguments.defult = arg_value
        return self.arguments

class UltronCommand:
    def __init__(
        self,
        namespace: UltronNameSpace,
        name: str,
        function: Callable,
        flags: Optional[UltronFlagParser] or None = None,
        arguments: Optional[UltronArgumentParser] or UltronArgumentParser or None = None,
        help: Optional[str] or None = None,
    ):
        """
        ### Class ultron command parser,
        #### takes the command name and if threre are arguments, flags and help message inside this command.
            * namespace: type(UltronNameSpace) The namespace scope.
            * command : type(str) command name.
            * flags : type(List[str] | str) By default this argument is None, but it passed as a list of str,
                e.g. `[flag, action, flag, action]` in order,
                note that when you pass this argument as a List you have to make sure to pass the type(action) == function.
            * arguments : flags : type(List[str] | str) By default this argument is None, but it passed as a list of str,
                e.g. `[arguement, action, arguement, action]` in order,
                note that when you pass this argument as a List you have to make sure to pass the type(action) == function.
            * help : type(str) a help message will be displayed when the end user pass {command --help} flag.
        """
        self.name = name
        self.namespace = namespace
        self.flags = self.__mapflags(flags)
        self.arguments = self.__maparguments(arguments)
        if help == None:
            help = "--"
        self.help = help
        self.function = function
        self.command = UltronCommandNameSpace(
            name=self.name,
            flags=self.flags,
            arguments=self.arguments,
            help=self.help,
            function=self.function,
        )
        namespace.add(self.command)

    def add_flag(
        self,
        name: str,
        function: Callable,
        args: List[Any] or None = None,
        help: str or None = None,
    ) -> UltronCommandNameSpace:
        if name in list(self.flags.keys()):
            return "Error"
        flag: UltronFlagParser = UltronFlagParser(
            name=name, function=function, args=args, help=help
        )
        self.flags[flag.name] = flag
        return self

    def __str__(self):
        if self.flags is None:
            flags = []
        else:
            flags: List[str] = [f"-{flag}" for flag in self.flags.keys()]
        return f"<UltronCommand command={self.command.name}, namespace={self.namespace.name}, function={self.function.__name__}, flags={flags}, args={self.args}, arguments={self.arguments}, help='{self.help}'>"

    def __mapflags(self, flags: List[UltronFlagParser] or UltronFlagParser or None) -> List[str]:
        if flags is not None:
            mapped_flags: Dict[str, UltronFlagParser] = {}
            if type(flags) == list:
                for flag in flags:
                    mapped_flags[flag.name] = flag
            else:
                mapped_flags[flags.name] = flags
            return mapped_flags
        return flags

    def __maparguments(self, arguments: List[UltronArgumentParser] or UltronArgumentParser or None) -> List[str]:
        if arguments is not None:
            mapped_arguments: Dict[str, UltronArgumentParser] = {}
            if type(arguments) == list:
                for argument in arguments:
                    mapped_arguments[argument.name] = argument
            else:
                mapped_arguments[arguments.name] = arguments
            return mapped_arguments
        return arguments
