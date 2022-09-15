# ultron-shell

* ultron-shell is a one of multiple powerful ultron packages.
* ultron-shell is a feature-rich command line parser for Python.
* ultron-shell supports positional arguments, flags, required arguments and more.
* ultron-shell automatically generates usage by passing help argument, help and error messages.


## usage

### Simple example:

```python
from ultron_shell import UltronCommandLine
from typing import Any

# Take an instance from UltronCommandLine
ultron: UltronCommandLine = UltronCommandLine()

# Call the add_command() method to add a new command to ultron name space.
init: Any = ultron.add_command(command='init', help='initial command to test if it works.')
add: Any = ultron.add_command(command='add', help="add command.")

# Then you can call add_argument method to pass new argument to an exact command.
# You can pass required = True in case if this argument is required to run the command.
ultron.add_argument(init, "--config", "config file to configure", required=True)
ultron.add_argument(add, "--path", "path of directory")

# in case you wrote a lot of code and you forget what the command containes.
ultron.get_command("add")
# in case you wrote a wrong command, you'll error hint into the terminal once you run.

# Also you can get all argument attrs [help, required, value] by using.
ultron.get_argument(add, "--path") # make sure that you passed the actual command varible.
# in case you wrote a wrong command, you'll error hint into the terminal once you run.
```

### OOP example
```python
from ultron_shell import UltronCommandLine
from typing import Any


class CommandLine(UltronCommandLine):
    def __init__(self):
        UltronCommandLine.__init__(self)
        self.init()

    def init(self):
        init:   Any = self.add_command("init", help="init command to initialize")
        pars:   Any = self.add_command("pars", help="parse names.")
        add:    Any = self.add_command("add", help="add config parser")

        self.add_argument(init, "--config", "config file to configure", required=True)
        self.add_argument(init, "--path", "path of directory")
        self.add_argument(pars, "--name", "name of config parser")

        self.get_command("add")
        self.get_argument(add, "name")
```