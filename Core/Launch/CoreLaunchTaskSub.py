import json
import os
import platform, re, subprocess
import threading
import urllib.request
import uuid
import hashlib

import FMCLCore.System.CoreMakeFolderTask
import FMCLCore.System.SystemAndArch
import FMCLCore.System.UnzipTask

def download_native(arg: dict):
    back_msg = threading.current_thread().name + " done with message: "
    e = 0
    emsg = ""
    for i in range(5):
        if os.path.exists(arg["path"]) and \
                (("size" not in arg) or (os.path.getsize(arg["path"]) == arg["size"])) and \
                (("sha1" not in arg) or (hashlib.sha1(open(arg["path"], "rb").read()).hexdigest() == arg["sha1"])):
            back_msg += f"Download successfully in {i} try(s) and {e} exception(s): {emsg}"
            break
        else:
            try:
                open(arg["path"], "wb+").write(urllib.request.urlopen(arg["url"], timeout=5).read())
                if "unzip" in arg:
                    print("unzip", arg)
                    FMCLCore.System.UnzipTask.unzip(arg["path"], arg["unzip"])
            except Exception as exc:
                e += 1
                emsg += repr(exc)
    print(back_msg)

def multprocessing_task(tasks: list, function, cores: int):
    threads = []

    def _run():
        while threads:
            try:
                task = tasks.pop()
                function(task)
            except IndexError:
                break

    for i in range(cores + 1):
        thread = threading.Thread(target=_run)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def _checkRules(rules: dict):
    for i in rules:
        if i["action"] == "allow":
            if "os" in i:
                if "name" in i["os"] and FMCLCore.System.SystemAndArch.system() != i["os"]["name"]:
                    return False
                elif "version" in i["os"] and not re.match(i["os"]["version"], platform.version()):
                    return False
        elif i["action"] == "disallow":
            if "os" in i:
                if "name" in i["os"] and FMCLCore.System.SystemAndArch.system() == i["os"]["name"]:
                    return False
                elif "version" in i["os"] and re.match(i["os"]["version"], platform.version()):
                    return False
    return True

def launch(game_directory: str = ".minecraft", version_name: str = None, java: str = "java", playername: str = "player",
           UUID: str = uuid.uuid4().hex, TOKEN: str = "0", JvmMaxMemory: int = 1024, FixMaxThread: int = 64):

    cmdlist = []

    basic_jvm = [{'rules': [{'action': 'allow', 'os': {'name': 'osx'}}], 'value': ['-XstartOnFirstThread']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows'}}], 'value': [
                     '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows', 'version': '^10\\.'}}],
                  'value': ['-Dos.name=Windows 10', '-Dos.version=10.0']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'unknown', 'arch': 'x86'}}], 'value': ['-Xss1M']},
                 '-Djava.library.path=${natives_directory}', '-Dminecraft.launcher.brand=${launcher_name}',
                 '-Dminecraft.launcher.version=${launcher_version}', '-cp', '${classpath}']

    game_directory = os.path.realpath(game_directory)

    verpath = os.path.join(game_directory, "versions", version_name)
    libpath = os.path.join(verpath, "natives-" + FMCLCore.System.SystemAndArch.system()) + "test"
    jsonpath = os.path.join(verpath, version_name + ".json")
    jarpath = os.path.join(verpath, version_name + ".jar")

    if version_name is None:
        return 0
    if not (os.path.exists(game_directory) and os.path.exists(jsonpath)):
        return 1

    ver_json = json.load(open(jsonpath))

    if "minecraftArguments" in ver_json:
        args = ver_json["minecraftArguments"].split(" ")

    elif "arguments" in ver_json and "game" in ver_json["arguments"]:
        args=[]
        for i in ver_json["arguments"]["game"]:
            if type(i) == str:
                args.append(i)
    else:
        args = ""

    cmdlist.append(java)

    if "arguments" in ver_json:
        for i in ver_json["arguments"]["jvm"]:
            if type(i) != str:
                if _checkRules(i["rules"]):
                    if type(i["value"]) == str:
                        cmdlist.append(i["value"])
                    else:
                        for j in i["value"]:
                            cmdlist.append(j)

            else:
                cmdlist.append(i)
    else:
        for i in basic_jvm:
            if type(i) != str:
                if _checkRules(i["rules"]):
                    for j in i["value"]:
                        cmdlist.append(j)
            else:
                cmdlist.append(i)

    cmdlist.append("-Xmx" + str(JvmMaxMemory) + "m")

    cmdlist.append("${mainClass}")
    cmdlist += args

    cp = ""
    need_to_be_fixed = []

    if not os.path.exists(jarpath):
        need_to_be_fixed.append({
            "path": jarpath,
            "url": ver_json["downloads"]["client"]["url"],
            "size": ver_json["downloads"]["client"]["size"],
            "sha1": ver_json["downloads"]["client"]["sha1"]})

    for i in ver_json['libraries']:
        if "name" in i:
            name = i["name"].split(":")  # <package>:<name>:<version>
            name[0] = name[0].replace(".", os.sep)
            p = name[0]
            n = name[1]
            v = name[2]
            rpath = os.path.join(game_directory, "libraries", p, n, v, n + "-" + v + ".jar")
            if ("rules" not in i) or _checkRules(i["rules"]):
                if ("downloads" not in i) or ("classifiers" not in i["downloads"]):
                    if "downloads" in i:
                        if "artifact" in i["downloads"]:
                            package = {
                                "path": os.path.join(game_directory, "libraries", i["downloads"]["artifact"]["path"]),
                                "url": i["downloads"]["artifact"]["url"],
                                "size": i["downloads"]["artifact"]["size"],
                                "sha1": i["downloads"]["artifact"]["sha1"]
                            }
                            FMCLCore.System.CoreMakeFolderTask.make_long_dir(os.path.dirname(package["path"]))
                            need_to_be_fixed.append(package)
                    elif "url" in i:
                        FMCLCore.System.CoreMakeFolderTask.make_long_dir(os.path.dirname(rpath))
                        need_to_be_fixed.append({
                            "path": rpath,
                            "url": i["url"] + p.replace("\\", "/") + "/" + n + "/" + v + "/" + n + "-" + v + ".jar"})
                    else:
                        print("Failed to fix depend:", rpath)


                    cp += os.path.realpath(rpath) + os.pathsep

                else:
                    if "natives-" + FMCLCore.System.SystemAndArch.system() in i["downloads"]["classifiers"]:
                        package = {
                            "path": os.path.join(game_directory, "libraries", i["downloads"]["classifiers"]["natives-" + FMCLCore.System.SystemAndArch.system()]["path"]),
                            "url": i["downloads"]["classifiers"]["natives-" + FMCLCore.System.SystemAndArch.system()]["url"],
                            "unzip": libpath,
                            "size": i["downloads"]["classifiers"]["natives-" + FMCLCore.System.SystemAndArch.system()]["size"],
                            "sha1": i["downloads"]["classifiers"]["natives-" + FMCLCore.System.SystemAndArch.system()]["sha1"]
                        }
                        FMCLCore.System.CoreMakeFolderTask.make_long_dir(os.path.dirname(package["path"]))
                        print("Fix library:", rpath)
                        need_to_be_fixed.append(package)

    multprocessing_task(need_to_be_fixed, download_native, FixMaxThread)

    cp += jarpath

    arg = {
        "${mainClass}": ver_json["mainClass"],
        "${natives_directory}": libpath,
        "${launcher_name}": "FMCL",
        "${launcher_version}": "Rebuild",
        "${classpath}": cp,
        "${assets_root}": os.path.realpath(os.path.join(game_directory, "assets")),
        "${assets_index_name}": ver_json["assetIndex"]["id"],
        "${auth_uuid}": UUID,
        "${auth_access_token}": TOKEN,
        "${user_type}": "Legacy",
        "${version_type}": "FMCL",
        "${user_properties}": "{}",
        "${auth_session}": "{}",
        "${clientid}": "0",
        "${auth_xuid}": "0",
        "${game_assets}": "resources",
        "${auth_player_name}": playername,
        "${version_name}": version_name,
        "${game_directory}": game_directory
    }
    for i in range(len(cmdlist)):
        for j in arg:
            if j in cmdlist[i]:
                cmdlist[i] = cmdlist[i].replace(j, arg[j])

    return cmdlist

#a = (launch(r"C:\Users\Sharll\Desktop\HMCL\.minecraft",
#                      "1.8.9",
#                      "java.exe",
#                      "sharll"))
#print(a)
#subprocess.run(a)
#input()
