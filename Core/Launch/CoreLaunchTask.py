import json
import os
import re
import uuid
import sys
import platform


def _system():
    _support = {"win32": 'windows', "linux": "linux", "darwin": "osx"}
    if sys.platform in _support:
        return _support[sys.platform]
    return sys.platform


def _checkRules(rules: dict):
    localos = _system()
    for i in rules:
        if i["action"] == "allow":
            if ("os" not in i) or ("name" in i["os"] and localos == i["os"]["name"]):
                if "os" in i and "version" in i["os"]:
                    if not re.match(i["os"]["version"], platform.version()):
                        return False
                return True
            else:
                return False

        elif i["action"] == "disallow":
            if ("os" not in i) or ("name" in i["os"] and localos == i["os"]["name"]):
                if "os" in i and "version" in i["os"]:
                    if not re.match(i["os"]["version"], platform.version()):
                        return True
                return False
            else:
                return True

        else:
            return -1


def launch(game_directory: str = ".minecraft", version_name: str = None, java: str = "java",
           auth_player_name: str = "player"):
    basic_jvm = [{'rules': [{'action': 'allow', 'os': {'name': 'osx'}}], 'value': ['-XstartOnFirstThread']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows'}}], 'value': [
                     '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows', 'version': '^10\\.'}}],
                  'value': ['-Dos.name=Windows 10', '-Dos.version=10.0']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'unknown', 'arch': 'x86'}}], 'value': ['-Xss1M']},
                 '-Djava.library.path=${natives_directory}', '-Dminecraft.launcher.brand=${launcher_name}',
                 '-Dminecraft.launcher.version=${launcher_version}', '-cp', '${classpath}']

    print(basic_jvm)

    game_directory = os.path.realpath(game_directory)

    verpath = os.path.join(game_directory, "versions", version_name)
    libpath = os.path.join(verpath, "natives-" + _system())
    jsonpath = os.path.join(verpath, version_name + ".json")
    jarpath = os.path.join(verpath, version_name + ".jar")

    if version_name is None:
        return 0
    if not (os.path.exists(game_directory) and os.path.exists(jsonpath)):
        return 1

    ver_json = json.load(open(jsonpath))

    if "minecraftArguments" in ver_json:
        args = ver_json["minecraftArguments"]

    elif "arguments" in ver_json and "game" in ver_json["arguments"]:
        args = ver_json["arguments"]["game"]
        atemp = ""
        for i in args:
            if type(i) == str:
                atemp += i + " "
        args = atemp

    else:
        args = ""

    basic_command = java + " "
    if "arguments" in ver_json:
        for i in ver_json["arguments"]["jvm"]:
            if type(i) != str:
                if _checkRules(i["rules"]):
                    if type(i["value"]) == str:
                        basic_command += i["value"] + " "
                    else:
                        for j in i["value"]:
                            basic_command += "\"" + j + "\" "

            else:
                basic_command += "\"" + i + "\" "

        basic_command += " ${mainclass} " + args

    else:
        for i in basic_jvm:
            if type(i) != str:
                if _checkRules(i["rules"]):
                    for j in i["value"]:
                        basic_command += "\"" + j + "\" "
            else:
                basic_command += "\"" + i + "\" "
        basic_command += " ${mainclass} " + args

    cp = ""

    for i in ver_json['libraries']:
        if "name" in i:
            if ("downloads" not in i) or ("classifiers" not in i["downloads"]):
                name = i["name"].split(":")  # <package>:<name>:<version>
                name[0] = name[0].replace(".", "/")
                p = name[0]
                n = name[1]
                v = name[2]
                rpath = os.path.join(game_directory, "libraries", p, n, v, n + "-" + v + ".jar")
                if ("rules" not in i) or (_checkRules(i["rules"])):
                    if os.path.exists(os.path.realpath(rpath)):
                        cp += os.path.realpath(rpath) + os.pathsep
                    else:
                        print(f"it seems that {rpath} do not exist.")

    cp += jarpath

    arg = {
        "${mainclass}": ver_json["mainClass"],
        "${natives_directory}": libpath,
        "${launcher_name}": "FMCL",
        "${launcher_version}": "k",
        "${classpath}": cp,
        "${assets_root}": os.path.realpath(os.path.join(game_directory, "assets")),
        "${assets_index_name}": ver_json["assetIndex"]["id"],
        "${auth_uuid}": uuid.uuid4().hex,
        "${auth_access_token}": "0",
        "${user_type}": "Legacy",
        "${version_type}": '"FMCL Preview 3"',
        "${user_properties}": "{}",
        "${auth_session}": "{}",
        "${clientid}": "0",
        "${auth_xuid}": "0",
        "${game_assets}": "resources",
        "${auth_player_name}": auth_player_name,
        "${version_name}": version_name,
        "${game_directory}": game_directory
    }

    for i in arg:
        basic_command = basic_command.replace(i, arg[i])

    return basic_command
