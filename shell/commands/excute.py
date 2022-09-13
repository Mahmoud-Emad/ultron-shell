from shell.commands.parser import UltronCommandLine
import sys


class CommandLine(UltronCommandLine):
    def __init__(self, argv: sys.argv):
        UltronCommandLine.__init__(self)
        self.argv = argv
        self.command = None
        self.args = None
        self.init()

    def excute(self):
        # pass
        return self.parse_args(self.argv)

    def init(self):
        init = self.add_command("init", help="init command to initialize")
        self.add_argument(
            init, "--config", "config file to configure", required=True
        )
        self.add_argument(init, "--path", "path of directory")
        add = self.add_command("add", help="add config parser")
        self.add_argument(add, "--name", "name of config parser")
        self.get_command("add")
        self.get_argument(add, "name")
        # print(add)
        # print(arg)
        # self.add_argument(add, "--cat", "cat file")
        # self.add_argument(add, "--remove", "remove files")
        # self.add_argument(
        #     add, "--clear-output-fast", "clear output directory to initialize new one"
        # )
        # self.excute()
