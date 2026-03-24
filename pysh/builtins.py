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
    if len(args) == 0:
        try:
            os.chdir(os.path.expanduser("~"))
        except Exception as e:
            print(f"cd error: {e}")
        return

    if len(args) > 1:
        print("Error: cd takes only one argument")
        print("Usage: cd <path>")
        return

    path = args[0]

    try:
        path = os.path.expanduser(path)
        os.chdir(path)

    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except NotADirectoryError:
        print(f"cd: not a directory: {path}")
    except PermissionError:
        print(f"cd: permission denied: {path}")
    except Exception as e:
        print(f"cd error: {e}")

#-------------------------------------------------------------------------------

def builtin_procinfo(args):
    try:
        import psutil
    except ImportError:
        print("Error: psutil module is required. Install with: pip install psutil")
        return

    if len(args) == 0:
        print("Error: procinfo requires a PID")
        print("Usage: procinfo <pid>")
        return

    if len(args) > 1:
        print("Error: procinfo takes only one argument")
        print("Usage: procinfo <pid>")
        return

    try:
        pid = int(args[0])
    except ValueError:
        print("Error: PID must be an integer")
        return

    try:
        proc = psutil.Process(pid)

        status = proc.status()
        memory = proc.memory_info().rss  
        cpu = proc.cpu_percent(interval=0.1)  
        ppid = proc.ppid()

        print(f"PID: {pid}")
        print(f"Status: {status}")
        print(f"CPU Usage: {cpu}%")
        print(f"Memory Usage: {memory} bytes")
        print(f"Parent PID: {ppid}")

    except psutil.NoSuchProcess:
        print(f"Error: No process with PID {pid}")
    except psutil.AccessDenied:
        print(f"Error: Access denied to process {pid}")
    except Exception as e:
        print(f"procinfo error: {e}")


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