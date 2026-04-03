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
    if len(args) == 0:
        print("Error: echo requires at least one argument")
        print("Usage: echo <text>")
        return

    print(" ".join(args))


#-------------------------------------------------------------------------------

def builtin_cd(args):
    path = args[0] if args else "~"
    try:
        os.chdir(os.path.expanduser(path))
    except Exception as e:
        print(f"cd: {e}")

#-------------------------------------------------------------------------------

def builtin_procinfo(args):
    if len(args) != 1:
        print("Usage: procinfo <pid>")
        return

    try:
        pid = int(args[0])
        with open(f"/proc/{pid}/status") as f:
            print(f.read())
    except ValueError:
        print("Error: PID must be an integer")
    except FileNotFoundError:
        print(f"Error: No process with PID {pid}")


#-------------------------------------------------------------------------------


def builtin_help(args):
    """
    Display a list of all available built-in commands and a brief description.
    """
    commands = {
        "pwd": "Print the current working directory.",
        "exit": "Exit the shell.",
        "touch": "Create a new empty file. Usage: touch <file name>",
        "echo": "Print text to the terminal. Usage: echo <text>",
        "cd": "Change the current directory. Usage: cd <path>",
        "procinfo": "Show information about a process. Usage: procinfo <pid>",
        "help": "Show this help message listing all built-in commands."
    }

    print("Available built-in commands:\n")
    for cmd, desc in commands.items():
        print(f"{cmd:<10} - {desc}")

#-------------------------------------------------------------------------------

def builtin_cat(args):
    if not args:
        print("Usage: cat <file> [file2 ...]")
        return

    for filename in args:
        try:
            with open(filename) as f:
                print(f.read(), end="")
        except FileNotFoundError:
            print(f"cat: {filename}: No such file or directory")
        except PermissionError:
            print(f"cat: {filename}: Permission denied")

#-------------------------------------------------------------------------------

def builtin_head(args):
    if not args:
        print("Usage: head [-n N] <file>")
        return

    n = 10
    if args[0] == "-n":
        try:
            n = int(args[1])
            args = args[2:]
        except (IndexError, ValueError):
            print("head: -n requires a valid integer argument")
            return

    for filename in args:
        try:
            with open(filename) as f:
                for line in f:
                    if n <= 0:
                        break
                    print(line, end="")
                    n -= 1
        except FileNotFoundError:
            print(f"head: {filename}: No such file or directory")
        except PermissionError:
            print(f"head: {filename}: Permission denied")

#-------------------------------------------------------------------------------

def builtin_wc(args):
    if not args:
        print("Usage: wc <file> [file2 ...]")
        return

    total_lines, total_words, total_chars = 0, 0, 0

    for filename in args:
        try:
            with open(filename) as f:
                content = f.read()
            lines = content.count("\n")
            words = len(content.split())
            chars = len(content)
            print(f"{lines:>8} {words:>8} {chars:>8} {filename}")
            total_lines += lines
            total_words += words
            total_chars += chars
        except FileNotFoundError:
            print(f"wc: {filename}: No such file or directory")
        except PermissionError:
            print(f"wc: {filename}: Permission denied")

    if len(args) > 1:
        print(f"{total_lines:>8} {total_words:>8} {total_chars:>8} total")

#-------------------------------------------------------------------------------