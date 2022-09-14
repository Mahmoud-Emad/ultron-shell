from typing import Dict, List

# from shell.commands.logger import Logger


class HelperHadler:
    @staticmethod
    def no_command_found(command: str, catched: bool or str = False):
        h: Logger = Logger.hint(message="-h")
        help: Logger = Logger.hint(message="--help")
        command: Logger = Logger.hint(message=command)
        if catched:
            return (
                f"There are no arguments named `{command}` {catched}\n "
                + f"- try to execute [{h}, {help}] to get help."
            )
        return (
            f"There are no arguments named `{command}`\n "
            + f"- try to execute [{h}, {help}] to get help."
        )

    @staticmethod
    def no_flag_found(command: str, flag: str):
        h: Logger = Logger.hint(message="-h")
        help: Logger = Logger.hint(message="--help")
        flag: Logger = Logger.hint(message=flag)
        command: Logger = Logger.hint(message=command)
        return (
            f"There are no flags named `{flag}` inside `{command}` command.\n "
            + f"- try to execute `{command}` [{h}, {help}] to get report of command flags."
        )

    @staticmethod
    def report_flags(report: Dict, help=None, command=None):
        command: Logger = Logger.hint(message=command, color="header")
        help: Logger = Logger.hint(message=help)
        msg: str = f"`{help}` flag, usage, `{Logger.hint(message=f'ultron {command}')}` {list(report.keys())}"
        Logger.log(
            color="success",
            message=Logger.hint(message=msg, color="doc"),
            message_with_color=f"Help {command}",
            end="",
        )
        for flag, _help in report.items():
            flag: Logger = Logger.hint(message=flag, color="header")
            _help: Logger = Logger.hint(message=_help, color="doc")
            Logger.log(
                color="doc",
                message_with_color="\tRun",
                message=Logger.hint(message=f"ultron {command} {flag} (" + _help + ")"),
                end="",
            )

    @staticmethod
    def report(report: Dict):
        Logger.log(
            color="doc",
            message_with_color="Help shell commands",
            message="",
            end="",
        )
        for command, values in report.items():
            command: Logger = Logger.hint(message=command, color="header")
            help: Logger = Logger.hint(message=values["help"], color="doc")

            Logger.log(
                color="doc",
                message_with_color="\tRun",
                message=Logger.hint(message=f"ultron {command} (" + help + ")"),
                end="",
            )
            for arg in values["args"]:
                flag: Logger = Logger.hint(message=arg["flag"], color="header")
                flag_help: Logger = Logger.hint(message=arg["help"], color="doc")
                Logger.log(
                    color="doc",
                    message_with_color="\tRun",
                    message=Logger.hint(
                        message=f"ultron {command} {flag} (" + flag_help + ")"
                    ),
                    end="",
                )

    @staticmethod
    def required_flag(command: str, flag: str):
        h: Logger = Logger.hint(message="-h")
        help: Logger = Logger.hint(message="--help")
        flag: Logger = Logger.hint(message=flag["flag"])
        command: Logger = Logger.hint(message=command)
        return (
            f"You can not excute `{command}` without `{flag}`.\n "
            + f"- try to execute `{command} {flag}` [{h}, {help}] to clear help of {command} usage."
        )
