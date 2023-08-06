import asyncio
from inspect import signature
from shella.term import Console

_cmds = []


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def run_command(argv):
    found = False
    for cmd in _cmds:
        if argv[0] in cmd.get("commands"):

            arg_template = cmd.get("arg_template")
            if arg_template:
                if not check_string_format(" ".join(argv[1:]), arg_template):
                    error(
                        f"Incorrect arguments, please provide on the format {arg_template}")
                    error(f"Command usage: {argv[0]} {cmd.get('usage')}")

                    return

            callback = cmd.get("callback")
            try:
                await callback(argv)
            except Exception:
                import traceback
                print("Command error")
                traceback.print_exc()
            found = True
    if not found:
        help()

c = Console(run_command)


def error(s):
    print(f"{bcolors.FAIL}ERROR: {s}{bcolors.ENDC}")


"""
Function decorator
"""


def shell_cmd(*args, **kwargs):
    def inner(func):
        o = {
        }

        o["commands"] = kwargs["commands"]
        if len(o["commands"]) > 2:
            error(
                f"Please provide at most two command alternatives. Found {len(o['commands'])} for {func.__name__}")

        o["desc"] = kwargs.get("desc", "-")
        o["arg_template"] = kwargs.get("template")
        o["usage"] = kwargs.get("usage", "?")

        o["callback"] = func

        sig = signature(func)
        if len(sig.parameters) != 1:
            error(
                f"Expected 1 argument for function <{func.__name__}> (This is where a list of the shell arguments are passed)")
        _cmds.append(o)
        c.commands.append(o["commands"][0])
        return func
    return inner


def check_string_format(string, format_string):
    try:
        values = string.split()
        if len(values) != len(format_string.split()):
            return False
        types = [s[-1] for s in format_string.split()]
        formatted_values = []
        for i, value in enumerate(values):
            if types[i] == "d":
                formatted_values.append(int(value))
            elif types[i] == "f":
                formatted_values.append(float(value))
            elif types[i] == "s":
                formatted_values.append(str(value))
            else:
                raise ValueError("Invalid format string")
        return True
    except ValueError as e:
        return False


@shell_cmd(commands=["help", "?"], desc="Prints help information")
async def help_cmd(argv):
    help()


def help():
    print(bcolors.OKBLUE+"Available commands are")
    print(bcolors.ENDC, end='')
    for cmd in _cmds:
        helpstr = ""
        for c in cmd.get("commands"):
            helpstr += f"{c} "
        helpstr = helpstr[:-1]
        print(f"{helpstr} \t: {cmd.get('desc')}")


running = True
shell_task_ref_ = None


async def shell_task():
    global shell_task_ref_
    global running
    shell_task_ref_ = asyncio.current_task()
    running = True
    await c.read_input_stream()
    print("EXIT")
    running = False


@shell_cmd(commands=["exit", "q"], desc="Prints help information")
async def exit_cmd(argv):
    global running
    running = False
    shell_task_ref_.cancel()
