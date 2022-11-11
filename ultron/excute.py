from ultron.shell.namespaces import UltronArgumentParser, UltronFlagParser
from ultron.shell.parser import UltronParser
import sys
import time


def sum(n1, n2):
    print("Function sum excuted.....")
    time.sleep(1)
    loading = " => loading"
    for i in range(21):
        time.sleep(0.1)
        sys.stdout.write("\r%d%%" % i)
        sys.stdout.flush()
        print(loading)
    print("Result = ", n1 + n2)


def remove_user(user):
    print(f"{user}, Deleted!")


def init_project(name: str = "Test", id=15) -> str:
    print("Intializing project")
    time.sleep(2)
    print("." * 50)
    time.sleep(2)
    print("Project Name = ", name)
    print("." * 50)
    time.sleep(3)
    print("Project initialized!")


def add_files_to_project():
    print("Files were added to project")


def stash_all_files(user_stash):
    print(f"User {user_stash} stash all files")


user = "Mahmoud"
parser = UltronParser()
command1_flag = UltronFlagParser(
    name="rm", function=sum, args=[1, 5], help="To delete user", required=True
)
command1_argument = UltronArgumentParser(
    name="name", defult="Test Project", help="Name of the project", required=False
)
command1_flag2 = UltronFlagParser(
    name="rf", function=remove_user, args=[user], help="To delete user"
)
command2_flag1 = UltronFlagParser(
    name="ps", function=remove_user, args=user, help="To delete user"
)
command1 = parser.add_command(
    name="init",
    flags=[command1_flag, command1_flag2],
    function=init_project,
    arguments=command1_argument
)

command2 = parser.add_command(
    name="add",
    help="This is a help message",
    function=add_files_to_project,
    flags=command2_flag1
).add_flag(name="-p", function=stash_all_files, args="Mahmoud Emad")

command2.add_flag(name="-ss", function=stash_all_files, args="ss")


def excute(argv=sys.argv[1:]):
    parser.parse(argv)
