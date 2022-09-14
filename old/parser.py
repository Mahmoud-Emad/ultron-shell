from typing import Any, List


class CommandLine:
    def __init__(self):
        self.commands = {}
        self.flags = []
        self.helps = []
        self.help_flags = ["-h", "--help"]

    def __str__(self):
        return f"""
            <UltronCommandLine commands={list(self.commands.keys())}>
        """.strip()

    def get(self, __name: str) -> Any:
        if self.commands.get(__name):
            command = self.commands.get(__name)
            return command

    def add_command(self, command: str, help: str):
        self.commands[command] = dict(help=help, args=[])
        return self.commands.get(command)

    def add_argument(
        self,
        command: "CommandLine",
        flag: str,
        help: str = None,
        required: bool = False,
    ):
        args: List[str] = command["args"]
        args.append(dict(flag=flag, help=help, required=required))

    def get_argument(self, arg):
        pass

    def parse_args(self, args: List[str]):
        flag: str = None
        _arg: str = None
        value: str = None

        for arg in args:
            if arg.lower().startswith("--") or arg.lower().startswith("-"):
                value = arg[arg.index("=") + 1 :]
                flag = arg.lower()
            elif not arg.lower().startswith("--") or not arg.lower().startswith("--"):
                _arg = arg.lower()

        print(flag)
        if _arg is None and flag in self.help_flags:
            return self.entry_point_report()
        elif _arg is None and flag not in self.help_flags:
            Logger.log(
                color="error",
                message=f"Flag `{Logger.hint(message=flag)}` not found, Available flags:",
                message_with_color="Uknown flag",
                end="",
            )
            return self.entry_point_report()
        elif not _arg and not flag:
            return self.entry_point_report()

        catched: str or bool = self.check_if_missing_characters(
            _arg, list(self.commands.keys())
        )

        if self.get(_arg):
            for _flag in self.get(_arg).get("args"):
                self.flags.append(list(_flag.values())[0])
                self.helps.append(list(_flag.values())[1])

            for _flag in self.get(_arg).get("args"):
                if (
                    _flag["required"] is True
                    and _flag["flag"] != flag
                    and flag not in self.help_flags
                ):
                    err = HelperHadler.required_flag(_arg, _flag)
                    return Logger.log(
                        color="error",
                        message=err,
                        message_with_color="Execution failed",
                    )

            if flag in self.help_flags:
                return self.help_flag(_arg, flag)
            elif flag in self.flags:
                pass
            elif flag and flag not in self.flags:
                err = HelperHadler.no_flag_found(_arg, flag)
                Logger.log(
                    color="error", message=err, message_with_color="Execution failed"
                )
        else:
            err = HelperHadler.no_command_found(_arg, catched=catched)
            Logger.log(
                color="error", message=err, message_with_color="Execution failed"
            )

    def check_if_missing_characters(self, _arg: str, args: List):
        found = False
        for arg in args:
            if (
                len(_arg) >= 2
                and _arg in arg
                or arg in _arg
                or _arg in arg
                or _arg[:-1] == arg[:-1]
                and _arg[-1] != arg[-1]
            ):
                found = True

            if found:
                return f"maybe you mean `{Logger.hint(message=arg)}`?"
        return False

    def help_flag(self, command, flag):
        args = self.flags
        helps = self.helps
        report: dict = {}
        for indx, arg in enumerate(args):
            report[arg] = helps[indx]
        return HelperHadler.report_flags(report, command=command, help=flag)

    def entry_point_report(self):
        return HelperHadler.report(self.commands)
