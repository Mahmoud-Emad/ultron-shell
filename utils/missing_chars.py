from typing import List, Dict


def find_argument(command: Dict, argument: str):
    args: List[str] = command["args"]  # list(.keys())
    return "name"
    # print(find_command(argument, args))


def find_command(command: str, commands: Dict) -> str:
    found_command: str or None = None
    commands: List[str] = list(commands)
    _command = ""
    founded_commands = []
    _len = 0
    for cmd in commands:
        for char in command:
            if _len >= len(cmd):
                break
            if cmd[_len] == char:
                _len += 1
                _command += char
        if len(_command) > 0:
            founded_commands.append(_command)
        _len = 0
        _command = ""

    big_len = 0
    _len = 0
    _command = ""
    if len(founded_commands) > 0:
        for cmd in founded_commands:
            if cmd == founded_commands[-1]:
                if len(cmd) > big_len:
                    _command = cmd
                break
            elif len(cmd) > len(founded_commands[_len + 1]):
                big_len = len(cmd)
                _command = cmd
            _len += 1
        big_len = 0
        for command in commands:
            if len(_command) > 1 and _command in command and len(command) > big_len:
                big_len = len(command)
                found_command = command
    return found_command
