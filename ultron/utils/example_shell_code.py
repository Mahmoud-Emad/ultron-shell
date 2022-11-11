from ultron.logger.log import Logger


def add_command_help(
    name: str,
    help: str,
    function: str,
    args: str,
    flag: None = None,
    flag_passed: bool = False,
    end: str = "\n",
):
    Logger.log(message="parser:", color="doc", end="")
    Logger.log(message="UltronParser", color="success", end="")
    Logger.log(message="=", color="white", end="")
    Logger.log(message="UltronParser", color="success", end="")
    Logger.log(message="()", color="doc", no_message_space=True, end="\n\t")
    Logger.log(message="parser.", color="doc")
    Logger.log(message="add_command", color="warning", no_message_space=True, end="")
    Logger.log(message="(", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="name =", color="doc", end="")
    Logger.log(message=f"'{name}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    if flag_passed:
        Logger.log(message="flags =", color="doc", end="")
        Logger.log(message=f"{flag}", color="blue", end="")
        Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="function =", color="doc", end="")
    Logger.log(message=f"{function}", color="warning", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="")
    Logger.log(
        message="# A callable function that will excute when the user call the command.",
        color="success",
        end="\n\t\t",
    )
    Logger.log(message="args =", color="doc", end="")
    Logger.log(message=f"'{args}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="")
    Logger.log(
        message="# If the passed function takes more than one argument pass it as a list.",
        color="success",
        end="\n\t\t",
    )
    Logger.log(message="help =", color="doc", end="")
    Logger.log(message=f"'{help}'", color="blue", end="\n\t")
    Logger.log(message=")", color="doc", no_message_space=True, end=end)


def flag_function_help(
    command_name: str, flag_name: str, function: str, args: str, help: str
):
    Logger.log(message="Hint:", color="header", end="\n\t")
    Logger.log(
        message="Every command you added can contains its flag and this flag contains its attributes, [function, name, required, args].",
        color="doc",
        end="\n\t",
    )
    Logger.log(message="So you can take an instance from", color="doc", end="")
    Logger.log(message="UltronFlagParser", color="success", end="")
    Logger.log(
        message="class then pass it when you register the command",
        color="doc",
        end="\n",
    )
    Logger.log(message="e.g.", color="header", end="\n\t")
    Logger.log(message=f"{command_name}_flag:", color="doc", end="")
    Logger.log(message="UltronFlagParser", color="success", end="")
    Logger.log(message="=", color="doc", end="")
    Logger.log(message="UltronFlagParser", color="success", end="")
    Logger.log(message="(", color="doc", end="\n\t\t")
    Logger.log(message="name =", color="doc", end="")
    Logger.log(message=f"'{flag_name}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="")
    Logger.log(
        message="# You can pass it starts with '-' or not, ultron smart to catch it ^_^.",
        color="success",
        end="\n\t\t",
    )
    Logger.log(message="function =", color="doc", end="")
    Logger.log(message=f"{function}", color="warning", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="args =", color="doc", end="")
    Logger.log(message=f"'{args}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="help =", color="doc", end="")
    Logger.log(message=f"'{help}'", color="blue", end="\n\t")
    Logger.log(message=" )", color="doc", no_message_space=True, end="\n\t")
    add_command_help(
        name=command_name,
        flag=f"{command_name}_flag",
        function=function,
        args=args,
        help=help,
        flag_passed=True,
    )
    return short_hand_flag(command_name, flag_name, function, args, help)


def short_hand_flag(
    command_name: str, flag_name: str, function: str, args: str, help: str
):
    Logger.log(message="Hint:", color="header", end="\n\t")
    Logger.log(
        message="Also you can use our short_hand_flag stracture to pass the flag, argument in one step.",
        color="doc",
        end="\n",
    )
    Logger.log(message="e.g.", color="header", end="\n\t")
    add_command_help(
        name=command_name,
        function=function,
        args="<Project name>",
        help="This is a help message.",
        end="",
    )
    Logger.log(message=".", no_message_space=True, color="doc", end="")
    Logger.log(message="add_flag", no_message_space=True, color="warning", end="")
    Logger.log(message="(", no_message_space=True, color="doc", end="\n\t\t")
    Logger.log(message="name =", color="doc", end="")
    Logger.log(message=f"'{flag_name}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="function =", color="doc", end="")
    Logger.log(message=f"{function}", color="warning", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="args =", color="doc", end="")
    Logger.log(message=f"'{args}'", color="blue", end="")
    Logger.log(message=",", color="doc", no_message_space=True, end="\n\t\t")
    Logger.log(message="help =", color="doc", end="")
    Logger.log(message=f"'{help}'", color="blue", end="\n\t")
    Logger.log(message=")", color="doc", no_message_space=True, end="\n")
    return wiki_help_link()


def wiki_help_link():
    Logger.log(
        message="You can read/see our wiki documentation at", color="doc", end=""
    )
    Logger.log(message="www.wiki.org/wiki/ultron-shell/", color="blue", end="\n\n")
