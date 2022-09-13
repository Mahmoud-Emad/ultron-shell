from shell.commands.excute import CommandLine
import sys


def excute(argv=sys.argv[1:]):
    CommandLine(argv)
