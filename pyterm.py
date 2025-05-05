import subprocess
import os
import pwd
import socket
import json
import sys
import psutil
import platform
from datetime import datetime

#print("-----------------\nYou have started the virtual terminal.\n-----------------")

original_dir = os.getcwd()
fullscreen_esc = True
new_neofetch = True

def bytes_to_MB(bytes):
    mb = bytes/(1024*1024)
    mb = int(mb)
    return str(mb)

def neofetch():
    print()
    print(pwd.getpwuid(os.getuid())[0] + "@" + platform.node())
    print("---------------")

    # prints the currently using system name
    print("[+] OS :", platform.system() + " " + platform.machine())

    # printing the Operating System release information
    print("[+] Kernel :", platform.release())

    # getting thesystem up time from the uptime file at proc directory
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()

    uptime = int(float(uptime))
    uptime_minutes = uptime // 60
    print("[+] Uptime : " + str(uptime_minutes) + " mins")

    # reading the cpuinfo file to print the name of
    # the CPU present
    with open("/proc/cpuinfo", "r") as f:
        file_info = f.readlines()

    cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name" in x]

    for index, item in enumerate(cpuinfo):
        if index == 0:
            item = item.split("@")
            if len(item) < 2:
                print("[+] CPU :" + item[0])
            else:
                print("[+] CPU :" + item[0] + "(" +
                      str(psutil.cpu_count(logical=True)) + ") " + "@" + item[1])

    # Using the virtual_memory() function it will return a tuple
    virtual_memory = psutil.virtual_memory()

    #This will print the primary memory details
    print("[+] Memory :",  bytes_to_MB(virtual_memory.used)
          + "Mib", "/", bytes_to_MB(virtual_memory.total) + "Mib")

    print()

def change_directory(command: str):
    try:
        dir = command[3:]

        if "\"" in command[3:]:
            dir = dir.split("\"")[1]
        elif "\'" in command[3:]:
            dir = dir.split("\'")[1]

        if "~" in dir:
            split = dir.split("~")
            dir = ""
            for l in range(0, len(split)):
                dir += split[l]
                if l < len(split)-1:
                    dir += "/home/" + pwd.getpwuid(os.getuid())[0]

        os.chdir(dir)
    except:
        pass

def history_logic(command: str, history: list, flscrn: dict):
    length = len(history)
    if length > 20:
        length = 20
    start = 0

    if command.startswith("history run"):
        if command != "history run":
            command = command.split(" ")[2]
            if command.isdigit():
                if int(command) in range(0, len(history)):
                    command = history[int(command)]
                else:
                    command = "none"
            elif command == "last":
                command = history[-1]

            if command != "none":
                history, flscrn = term_process(command, history, flscrn)
    else:
        if command != "history":
            if ":" in command:
                args = command.split(" ")[1]
                args = args.split(":")
                if args[0].isdigit() and args[1].isdigit():
                    start = int(args[0])
                    length = int(args[1])+1
            else:
                arg = command.split(" ")[1]
                if arg.isdigit():
                    if int(arg) < length:
                        start = length - int(arg)
                elif "-" in arg and arg.split("-")[1].isdigit():
                    if int(arg.split("-")[1]) < length:
                        length = int(arg.split("-")[1])

        for i in range(start, length):
            print(" ", i, history[i])
    
    return history, flscrn

def term_process(command: str, history: list, flscrn: dict):

    if command.startswith("cd"):
        history.append(command)
        change_directory(command)
    
    elif command.startswith("whoami"):
        print(pwd.getpwuid(os.getuid())[0] + " (on PyTerm)")

    elif command.startswith("history"):
        history, flscrn = history_logic(command, history, flscrn)

    elif command.startswith("add-flscrn"):
        flscrn_list = flscrn['flscrn']
        flscrn_list.append(command.split(" ")[1])
        flscrn['flscrn'] = flscrn_list

        savedata(original_dir + "/" + ".flscrn.json", flscrn)
    elif command.startswith("neofetch") and new_neofetch == True:
        history.append(command)
        neofetch()
    else:
        try:
            subprocess.run(command, shell=True)
            history.append(command)
        except:
            print("For some reason the command didn't work. Sorry about that.")

    if command.split(" ")[0] in flscrn['flscrn'] and fullscreen_esc == True:
        subprocess.run("clear", shell=True)

    return history, flscrn

def savedata(file: str, data: dict):
  "removes old file and then replaces it with fresh data @tpowell11"
  os.remove(file)  # delete outdated data
  dumpData = json.dumps(data)
  with open(file, 'w') as f:  # open file
    f.write(dumpData)  # write the new json

if os.path.exists('.flscrn.json') == False:
    flscrn = {'flscrn': ["nano", "top", "cmatrix", "vim", "htop", "lynx", "netris", "petris"]}
    subprocess.run("touch .flscrn.json", shell=True)
    savedata(".flscrn.json", flscrn)

with open('.flscrn.json', 'r') as myfile:
  data = myfile.read()
  flscrn = json.loads(data)  # global file open

for i in sys.argv:
    if i == "--no-fullscreen":
        fullscreen_esc = False
    elif i == "--og-neofetch":
        new_neofetch = False

history = []

if fullscreen_esc == True:
    subprocess.run("clear", shell=True)

while True:
    pretty_print_dir = os.getcwd()
    if os.getcwd().startswith("/home/" + pwd.getpwuid(os.getuid())[0]):
        pretty_print_dir = "~" + \
            str(os.getcwd())[len("/home/" + pwd.getpwuid(os.getuid())[0]):]

    command = input(pwd.getpwuid(os.getuid())[
                    0] + "@" + socket.gethostname() + ":" + pretty_print_dir + "$ ")
    
    if command == "exit":
        break

    history, flscrn = term_process(command, history, flscrn)

print("-----------------\nYou are no longer in the virtual terminal.\n-----------------")