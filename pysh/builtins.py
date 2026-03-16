"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
Look at builtin_pwd below as a complete example to follow.
"""

import os
import sys


# ---------------------------------------------------------------------------
# Example built-in: pwd
# ---------------------------------------------------------------------------


def builtin_pwd(args):
    """
    Print the current working directory.

    Uses os.getcwd() which asks the operating system for the current
    working directory of this process.

    Example usage:
        pysh /home/student $ pwd
        /home/student
    """
    print(os.getcwd())


# ---------------------------------------------------------------------------
# Example built-in: exit
# ---------------------------------------------------------------------------


def builtin_exit(args):
    """
    Exit the shell.

    Raises SystemExit which is caught by the main loop in shell.py
    to break out of the loop cleanly.
    """
    sys.exit(0)


# ---------------------------------------------------------------------------
# TODO: Implement the remaining built-in commands below.
#       Each function receives a list of string arguments.
#       Look at builtin_pwd above as an example to follow.
# ---------------------------------------------------------------------------



def builtin_touch(args):
    if len(args) == 0:
        print("Error you must enter a valid file name")
        print("Usage: touch <file name>")
        return

    if len(args) > 1:
        print("Error: you can only enter one valid file name")

    file_name = args[0]
    with open(file_name, "w") as f:
        f.write("")


#-------------------------------------------------------------------------------


def builtin_echo(args):
    if len (args) == 0:
        print("Error: you must enter a valid argument")
        print("Usage: echo <type argument here>")
        return
    else:
        print(" ".join(args))