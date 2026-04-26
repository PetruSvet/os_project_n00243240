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
import psutil
import time
import threading
import queue
import requests
import os
import platform
from urllib.parse import urlparse

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
    if len(args) != 1:                         # If the argument is not equal to 1
        print("Usage: procinfo <pid>")         # Print out how to use the command
        return

    try:
        pid = int(args[0])                     # the first element of the list of args given and convert the list of args into a int
        with open(f"/proc/{pid}/status") as f: # "with" checks if the code associated finished running and closes the file if so
            for line in f:
                if line.startswith('State'):
                    print(line.strip())
                if line.startswith('VmRSS'):
                    value = line.replace('VmRSS:', '').strip()
                    print("Memory usage:", value)
                if line.startswith('PPid'): 
                    print(line.strip())
        with open(f"/proc/{pid}/stat") as f:
            data = f.read().split()
            stime = int(data[14])
            ticks_per_sec = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
            stime_seconds = stime / ticks_per_sec
            print("Kernel CPU time (seconds):", stime_seconds)
    except ValueError:                          # If the args enterted is not a number then the int function returns value error
        print("Error: PID must be an integer")
    except FileNotFoundError:                   # If the file being found does not exist then inform the user it doesnt
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
        "cat <file1> <file2>": "Read and display contents of one or more files",
        "head <-n N> <file>": "Display the first <N> lines of a file",
        "wc <file1> <file2>": "Count lines, words and characters in one or more files",
        "sysinfo": "Shows real-time system resource usage",
        "download <file> -w <number>": "Download files using worker threads",
        "specs": "Show the operating system's hardware specifications",
    }

    print("Available built-in commands:\n")
    for cmd, desc in commands.items():
        print(f"{cmd:<30} - {desc}")

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

def builtin_sysinfo(args=None):   ##sysinfo --sort cpu
    sort_by = "memory"
    interval = 2                  ##sorts processes by memory and refresh every 2 secs

    # Parse arguments
    if args:
        if "--sort" in args:
            i = args.index("--sort")
            if i + 1 < len(args):
                sort_by = args[i + 1]

        if "--interval" in args:
            i = args.index("--interval")
            if i + 1 < len(args):
                interval = float(args[i + 1])

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            # -------- MEMORY --------
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            print("=== MEMORY ===")
            print(f"Total:     {mem.total // (1024**2)} MB")
            print(f"Used:      {mem.used // (1024**2)} MB")
            print(f"Available: {mem.available // (1024**2)} MB")
            print(f"Usage:     {mem.percent}%")

            print("\n=== SWAP ===")
            print(f"Total:     {swap.total // (1024**2)} MB")
            print(f"Used:      {swap.used // (1024**2)} MB")
            print(f"Free:      {swap.free // (1024**2)} MB")
            print(f"Usage:     {swap.percent}%")

            # -------- CPU --------
            print("\n=== CPU ===")
            print(f"Total CPU Usage: {psutil.cpu_percent()}%")

            per_core = psutil.cpu_percent(percpu=True)
            for i, usage in enumerate(per_core):
                print(f"Core {i}: {usage}%")

            # -------- PROCESSES --------
            print("\n=== TOP PROCESSES ===")

            processes = []
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(p.info)
                except:
                    pass

            key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
            processes = sorted(processes, key=lambda x: x[key], reverse=True)

            print(f"{'PID':<8}{'Name':<20}{'CPU %':<10}{'MEM %':<10}")
            print("-" * 50)

            for p in processes[:10]:
                print(f"{p['pid']:<8}{(p['name'] or '')[:18]:<20}{p['cpu_percent']:<10}{p['memory_percent']:.2f}") ## prints each process by PID, name (shortened to 18 characters only), cpu %, memory % (to 2 decimal places)

            time.sleep(interval) ## waits before refreshing again 2 secs


    except KeyboardInterrupt:
        print("\nExiting sysinfo...") ## when user does ctrcl + c it stops the process
#-----------------------------------------------------------------------------------------------------------------------




download_queue = queue.Queue()
completed_count = 0
counter_lock = threading.Lock()
workers = []
active = False

def worker():
    global completed_count

    while True:
        try:
            url = download_queue.get(timeout=1)
        except queue.Empty:
            break  # No more work

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            # Extract filename from URL
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "downloaded_file"

            os.makedirs("downloads", exist_ok=True)
            filepath = os.path.join("downloads", filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            with counter_lock:
                completed_count += 1

            print(f"[✓] Downloaded: {filename}")

        except Exception as e:
            print(f"[!] Failed: {url} ({e})")

        finally:
            download_queue.task_done()


def builtin_download(args=None):
    global workers, active

    if not args:
        print("Usage: download <file> [-w num] OR download --status")
        return

    if "--status" in args:
        print("\n=== DOWNLOAD STATUS ===")
        print(f"Queued: {download_queue.qsize()}")
        print(f"Workers: {len(workers)}")
        print(f"Completed: {completed_count}")
        print(f"Active: {any(w.is_alive() for w in workers)}")
        return

    file = args[0]
    num_workers = 3

    if "-w" in args:
        i = args.index("-w")
        if i + 1 < len(args):
            num_workers = int(args[i + 1])

    try:
        while not download_queue.empty():
            download_queue.get()

        with open(file) as f:
            for line in f:
                download_queue.put(line.strip())
                
    except FileNotFoundError:
        print("File not found.")
        return

    workers = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        workers.append(t)

    def monitor():
        download_queue.join()
        print("\nAll downloads completed.")

        threading.Thread(target=monitor, daemon=True).start()

    print(f"Started downloading with {num_workers} workers.")

    #------------------------------------------------------------------------------------------------------

def builtin_specs(args=None):
    print("=== SYSTEM SPECS ===\n")

    print("OS:", platform.system(), platform.release())
    print("Kernel:", platform.version())

    print("\n=== CPU ===")
    print("Processor:", platform.processor())
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Logical cores:", psutil.cpu_count(logical=True))

    freq = psutil.cpu_freq()
    if freq:
        print(f"Max Frequency: {freq.max:.2f} MHz")

    print("\n=== MEMORY ===")
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total // (1024**3)} GB")

    print("\n=== STORAGE ===")
    disk = psutil.disk_usage('/')
    print(f"Total Disk: {disk.total // (1024**3)} GB")

    print("\n=== MACHINE ===")
    print("Architecture:", platform.machine())