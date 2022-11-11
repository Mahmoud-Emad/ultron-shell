from typing import Any, List, Optional, Dict, Callable, Tuple
from ultron.logger.log import Logger
from ultron.shell.exeptions import ErrorHandler

from ultron.shell.namespaces import (
    UltronArgumentParser,
    UltronCommand,
    UltronFlagParser,
    UltronNameSpace,
)
from ultron.utils.enums import CommandLineTypes
from ultron.utils.missing_chars import find_command


class UltronParser:
    def __init__(self):
        self.namespace = UltronNameSpace()
        self.command = None
        self.flag = None
        self.argument = None
        self.help = None
        self.help_flags = ["--help", "-h"]
        self.error_catched = False

    def add_command(
        self,
        name: str,
        function: Callable,
        flags: Optional[List[UltronFlagParser]] or UltronFlagParser or None = None,
        arguments: Optional[List[UltronArgumentParser]]
        or UltronArgumentParser
        or None = None,
        help: Optional[List[str]] or None = None,
    ):
        if type(flags) == list or type(flags) == UltronFlagParser or flags is None:
            return UltronCommand(
                self.namespace,
                name=name,
                flags=flags,
                arguments=arguments,
                function=function,
                help=help,
            )
        raise TypeError(
            f"Cannot use type({type(flags).__name__}) as type(UltronFlagParser)"
        )

    def __flags(self, args: List[str]) -> List[str]:
        """Iterate over the incoming flags and return any flag passed"""
        flags: List[str] = []
        for flag in args:
            if flag.startswith("-") and not flag.startswith("--"):
                flags.append(flag.replace("-", ""))
        return flags

    def __arguments(self, args: List[str]) -> List[Dict]:
        """Iterate over the incoming arguments and return any argument passed"""
        arguments: List[Dict] = []
        for argument in args:
            if argument.startswith("--"):
                if argument in self.help_flags:
                    return
                if "=" in argument:
                    key, value = argument.split("=")
                    if len(value) > 0:
                        arguments.append({key.replace("--", ""): value})
                    else:
                        self.error_catched = True
                        return ErrorHandler.missing_argument_format(argument, args[0])
                else:
                    self.error_catched = True
                    return ErrorHandler.missing_argument_format(argument, args[0])
        return arguments

    def __clean(self, argv: List[str]) -> List[str]:
        """Remove all arguments, flags from the incoming list parser"""
        new_args: List[str] = []
        for argument in argv:
            if (
                not argument.startswith("-")
                and not argument.startswith("--")
                or argument in self.help_flags
            ):
                new_args.append(argument)
        return new_args

    def parse(self, argv: List[str]):
        arguments: List[Dict] = self.__arguments(argv)
        flags: List[str] = self.__flags(argv)
        argv = self.__clean(argv)  # remove flags and arguments, and leave only command.
        if not self.error_catched:
            if len(argv) == 1 and argv[0] in self.help_flags:
                # Help Commands
                return ErrorHandler.entry_point_help(
                    self.namespace.commands.__from_namespace__()
                )
            elif len(argv) == 0:
                return ErrorHandler.entry_point_help(
                    self.namespace.commands.__from_namespace__()
                )
            if len(argv) <= 2:
                if (
                    len(argv) > 1
                    and argv[0] in self.namespace.commands.all()
                    and argv[1] in self.help_flags
                ):
                    # Help Hint
                    print("Yes")
                elif len(argv) == 1:
                    command: str = argv[0]
                    if argv[0] not in self.namespace.commands.all():
                        if find_command(argv[0], self.namespace.commands.all()):
                            return ErrorHandler.did_you_men(
                                command,
                                find_command(command, self.namespace.commands.all()),
                                CommandLineTypes.command.value,
                            )
                        return ErrorHandler.command_not_found(command)
                    command = self.namespace.commands.get(command)
                    if (
                        command.has_required_flags()
                        and command.get_required_flag().name not in flags
                    ):
                        return ErrorHandler.is_required(
                            command.name,
                            command.get_required_flag().name,
                            type=CommandLineTypes.flag.value,
                        )
                    for flag in flags:
                        if (
                            not command.__getattr__("flags")
                            or flag not in command.__getattr__("flags").keys()
                        ):
                            return ErrorHandler.flag_not_found(command.name, flag)

                    check_and_register: Tuple(bool, str) = command.register_arguments(arguments)
                    if type(check_and_register) is tuple and check_and_register[0] is False:
                        return ErrorHandler.unknown_argument(
                            argument = check_and_register[1],
                            command = command.name
                        )
                    command.extract_arguments_and_do_action()

                    for flag in flags:
                        if command.__getattr__("flags").get(flag).args is None:
                            command.__getattr__("flags").get(flag).function()
                        else:
                            if (
                                type(command.__getattr__("flags").get(flag).args)
                                == list
                            ):
                                command.__getattr__("flags").get(flag).function(
                                    *command.__getattr__("flags").get(flag).args
                                )
                            else:
                                command.__getattr__("flags").get(flag).function(
                                    command.__getattr__("flags").get(flag).args
                                )
                else:
                    command_hint = Logger.hint("ultron --help/-h")
                    Logger.error(header="Parse Error", message="too many commands")
                    Logger.help(
                        header="Help Hint",
                        message=f"You can excute {command_hint} to get full report.",
                    )
            else:
                return ErrorHandler.too_much_commands(argv)