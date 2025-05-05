import subprocess
import os
import getpass
import socket
import json
import sys
import psutil
import platform
import argparse
from datetime import datetime

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="PyTerm - A virtual terminal emulator.")
parser.add_argument(
    "--no-fullscreen",
    action="store_true",
    help="Disable fullscreen clear on specified commands.",
)
parser.add_argument(
    "--og-neofetch", action="store_true", help="Use original neofetch output."
)
args = parser.parse_args()

fullscreen_esc = not args.no_fullscreen
new_neofetch = not args.og_neofetch

# --- Setup ---
original_dir = os.getcwd()
username = getpass.getuser()
home_dir = os.path.expanduser("~")
flscrn_file = os.path.join(original_dir, ".flscrn.json")


def bytes_to_MB(bytes_val):
    return str(int(bytes_val / (1024 * 1024)))


def neofetch():
    print()
    print(f"{username}@{platform.node()}")
    print("---------------")
    print(f"[+] OS     : {platform.system()} {platform.machine()}")
    print(f"[+] Kernel : {platform.release()}")

    with open("/proc/uptime", "r") as f:
        uptime = int(float(f.read().split(" ")[0].strip()))
        print(f"[+] Uptime : {uptime // 60} mins")

    with open("/proc/cpuinfo", "r") as f:
        file_info = f.readlines()
    cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name" in x]
    if cpuinfo:
        item = cpuinfo[0].split("@")
        cpu_str = item[0].strip()
        if len(item) > 1:
            cpu_str += f" ({psutil.cpu_count(logical=True)}) @ {item[1].strip()}"
        print(f"[+] CPU    : {cpu_str}")

    mem = psutil.virtual_memory()
    print(f"[+] Memory : {bytes_to_MB(mem.used)} MiB / {bytes_to_MB(mem.total)} MiB\n")


def change_directory(command, *_):
    try:
        path = command.strip()[3:].strip().strip("'\"")
        path = os.path.expanduser(path)
        os.chdir(path)
    except Exception as e:
        print(f"Failed to change directory: {e}")


def do_whoami(command, *_):
    print(f"{username} (on PyTerm)")


def history_logic(command, history, flscrn):
    if command.startswith("history run"):
        parts = command.split()
        if len(parts) >= 3:
            index = parts[2]
            if index == "last":
                run_cmd = history[-1]
            elif index.isdigit() and int(index) < len(history):
                run_cmd = history[int(index)]
            else:
                print("Invalid history index.")
                return history, flscrn
            history, flscrn = term_process(run_cmd, history, flscrn)
    else:
        max_items = 20
        items = history[-max_items:]
        for i, cmd in enumerate(items):
            print(f" {len(history) - len(items) + i}: {cmd}")
    return history, flscrn


def add_flscrn(command, history, flscrn):
    parts = command.split()
    if len(parts) >= 2:
        flscrn["flscrn"].append(parts[1])
        savedata(flscrn_file, flscrn)


def savedata(file, data):
    try:
        with open(file, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Failed to save data: {e}")


def term_process(command, history, flscrn):
    cmd_name = command.strip().split()[0]

    COMMANDS = {
        "cd": change_directory,
        "whoami": do_whoami,
        "history": history_logic,
        "add-flscrn": add_flscrn,
        "neofetch": lambda *args: neofetch() if new_neofetch else None,
    }

    if cmd_name in COMMANDS:
        COMMANDS[cmd_name](command, history, flscrn)
        if cmd_name != "history":  # avoid double-saving history
            history.append(command)
    else:
        try:
            subprocess.run(command, shell=True)
            history.append(command)
        except Exception as e:
            print(f"Command failed: {e}")

    if cmd_name in flscrn["flscrn"] and fullscreen_esc:
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    return history, flscrn


def main():
    # --- Init flscrn ---
    if not os.path.exists(flscrn_file):
        flscrn = {
            "flscrn": [
                "nano",
                "top",
                "cmatrix",
                "vim",
                "htop",
                "lynx",
                "netris",
                "petris",
            ]
        }
        savedata(flscrn_file, flscrn)
    else:
        with open(flscrn_file, "r") as f:
            flscrn = json.load(f)

    history = []

    if fullscreen_esc:
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    while True:
        try:
            cwd = os.getcwd()
            display_path = (
                cwd.replace(home_dir, "~") if cwd.startswith(home_dir) else cwd
            )
            command = input(
                f"{username}@{socket.gethostname()}:{display_path}$ "
            ).strip()
            if command == "exit":
                break
            if command:
                history, flscrn = term_process(command, history, flscrn)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting PyTerm.")
            break

    print(
        "-----------------\nYou are no longer in the virtual terminal.\n-----------------"
    )


if __name__ == "__main__":
    main()
