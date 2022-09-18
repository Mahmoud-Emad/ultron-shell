from shell.commands.parser import UltronCommandLine
import sys


class CommandLine(UltronCommandLine):
    def __init__(self, argv: sys.argv):
        UltronCommandLine.__init__(self, argv)
        self.init()

    def init(self):
        init = self.add_command("init", help="init command to initialize")
        pars = self.add_command("pars", help="parse names.")
        add = self.add_command("add", help="add config parser")
        config = self.add_argument(
            add, "--config", "config file to configure", required=True
        )
        _config = self.add_argument(
            init, "--config_in_path", "config file to configure", required=True
        )
        self.add_argument(init, "--path", "path of directory")
        # name = self.add_argument(pars, "--name", "name of config parser")
        # self.get_command("add")
        # print(self.get_value(pars, name))
        # print(self.set_value(pars, name, "test"))
        # print(self.get_value(pars, name))
        # self.delete(pars)
        # self.get_command("pars")
        # print(self.commands())
        # print(self.arguments(add))
        # self.get_argument(pars, "name")
        # print(add)
        self.parse_args()
