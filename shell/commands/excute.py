from shell.commands.parser import UltronCommandLine
import sys


class CommandLine(UltronCommandLine):
    def __init__(self, argv: sys.argv):
        UltronCommandLine.__init__(self)
        self.argv = argv
        self.command = None
        self.args = None
        self.init()

    def init(self):
        init = self.add_command("init", help="init command to initialize")
        pars = self.add_command("pars", help="parse names.")
        add = self.add_command("add", help="add config parser")
        self.add_argument(init, "--config", "config file to configure", required=True)
        self.add_argument(init, "--path", "path of directory")
        self.add_argument(pars, "--name", "name of config parser")
        self.get_command("add")
        self.get_argument(add, "name")