import platform
import subprocess

import colorama as co
import Const
import Core.Launch.CoreLaunchTaskSub
import Core.System.CoreConfigIO
import Core.System.CoreVersionGet

def Split(string: str):
    ed = [""]
    in_str = False
    mul_space = False
    for k in range(len(string)):
        char = string[k]
        if in_str:
            if char == "\"":
                in_str = False
            else:
                ed.append(ed.pop() + char)
        else:
            if char == " ":
                if not mul_space:
                    ed.append("")
                    mul_space = True
            else:
                mul_space = False
                if char == "\"":
                    in_str = True
                else:
                    ed.append(ed.pop() + char)
    return ed

co.init()
print(co.Fore.MAGENTA + "##" + co.Fore.GREEN + "######" + co.Style.RESET_ALL + "\t" + "Welcome to FMCL " + Const.software_version)
print(co.Fore.MAGENTA + "##" + co.Fore.GREEN + "######" + co.Style.RESET_ALL + "\t" + "Running on Python " + platform.python_version())
print(co.Fore.MAGENTA + "##" + co.Fore.WHITE + "####" + co.Fore.CYAN + "##" + co.Style.RESET_ALL + "\t" + "Operating system:\t" + platform.system() + "(RAW)/" + Core.Launch.CoreLaunchTaskSub.system())
print(co.Fore.MAGENTA + "##" + co.Fore.WHITE + "####" + co.Fore.CYAN + "##" + co.Style.RESET_ALL + "\t" + "System Architect:\t" + platform.machine() + "(RAW)/" + Core.Launch.CoreLaunchTaskSub.arch())
print(co.Fore.YELLOW + "######" + co.Fore.CYAN + "##" + co.Style.RESET_ALL + "\t" + "Source on github:\t" + "https://github.com/Sharll-large/FMCL")
print(co.Fore.YELLOW + "######" + co.Fore.CYAN + "##" + co.Style.RESET_ALL + "\t" + "If you don't know what to do, input \"help\" for a command list.")

print(co.Style.RESET_ALL + "Start checking configure file...")
Core.System.CoreConfigIO.fixdepend()
conf = Core.System.CoreConfigIO.read()

while True:
    line = Split(input("FMCL " + conf[".mc"] + ">"))
    command = line[0]
    if len(command) > 1: args = line[1:]
    else: args = []
    if command == "cd" and len(args) >= 1:
        conf[".mc"] = args[0]
    elif command == "cdjava" and len(args) >= 1:
        conf["java"] = args[0]
    elif command == "rename" and len(args) >= 1:
        conf["playername"] = args[0]
    elif command == "launch" and len(args) >= 1:
        subprocess.run(Core.Launch.CoreLaunchTaskSub.launch(conf[".mc"], args[0], conf["java"], conf["playername"]))
    elif command == "scan":
        for i in Core.System.CoreVersionGet.local_version(conf[".mc"]):
            print(i)
    elif command == "exit":
        break


Core.System.CoreConfigIO.writejson(conf)
