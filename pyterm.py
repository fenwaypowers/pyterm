import subprocess, os, pwd, socket, json, sys

#print("-----------------\nYou have started the virtual terminal.\n-----------------")

original_dir = os.getcwd()
fullscreen_esc = True

def savedata(file: str, data: dict):
  "removes old file and then replaces it with fresh data @tpowell11"
  os.remove(file)  # delete outdated data
  dumpData = json.dumps(data)
  with open(file, 'w') as f:  # open file
    f.write(dumpData)  # write the new json

if os.path.exists('.flscrn.json') == False:
    flscrn = {'flscrn': ["nano", "top", "cmatrix", "vim", "htop", "lynx"]}
    subprocess.run("touch .flscrn.json", shell=True)
    savedata(".flscrn.json", flscrn)

with open('.flscrn.json', 'r') as myfile:
  data = myfile.read()
  flscrn = json.loads(data)  # global file open

for i in sys.argv:
    if i == "--no-fullscreen":
        fullscreen_esc = False

history = []

while True:
    pretty_print_dir = os.getcwd()
    if os.getcwd().startswith("/home/" + pwd.getpwuid(os.getuid())[0]):
        pretty_print_dir = "~" + str(os.getcwd())[len("/home/" + pwd.getpwuid(os.getuid())[0]):]

    command = input(pwd.getpwuid(os.getuid())[0] + "@" + socket.gethostname() + ":" + pretty_print_dir + "$ ")
    
    if command.startswith("cd"):
        history.append(command)
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
    elif command == "exit":
        break
    elif command.startswith("history"):
        length = len(history)
        start = 0
        
        if command != "history":
            arg = command.split(" ")[1]
            if arg.isdigit():
                if int(arg) < length:
                    start = length - int(arg)
            elif "-" in arg and arg.split("-")[1].isdigit():
                if int(arg.split("-")[1]) < length:
                    length = int(arg.split("-")[1])

        for i in range(start, length):
            print(history[i])
    elif command.startswith("add-flscrn"):
        flscrn_list = flscrn['flscrn']
        flscrn_list.append(command.split(" ")[1])
        flscrn['flscrn'] = flscrn_list

        savedata(original_dir + "/" + ".flscrn.json", flscrn)
    else:
        if command.startswith("neofetch") and fullscreen_esc == True:
            subprocess.run("clear", shell=True)

        try:
            process = subprocess.run(command, shell=True)
            history.append(command)
        except:
            print("For some reason the command didn't work. Sorry about that.")
    
    if command.split(" ")[0] in flscrn['flscrn'] and fullscreen_esc == True:
        subprocess.run("clear", shell=True)

print("-----------------\nYou are no longer in the virtual terminal.\n-----------------")