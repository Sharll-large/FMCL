# coding:utf-8
"""
    启动游戏
"""
import json
import os
import platform
import re
import subprocess

import core.auth.oauth
import core.system.SystemAndArch


def _checkRules(rules: dict):
    for i in rules:
        if i["action"] == "allow":
            if "os" in i:
                if "name" in i["os"] and core.system.SystemAndArch.system() != i["os"]["name"]:
                    return False
                elif "version" in i["os"] and not re.match(i["os"]["version"], platform.version()):
                    return False
        elif i["action"] == "disallow":
            if "os" in i:
                if "name" in i["os"] and core.system.SystemAndArch.system() == i["os"]["name"]:
                    return False
                elif "version" in i["os"] and re.match(i["os"]["version"], platform.version()):
                    return False
    return True


def launch(game_directory: str, version_name: str, account: dict,
           java_path: str = "java", java_ram: int = 1024, use_jvm_for_performance: bool = False,
           standalone: bool = False):
    cmdlist = []

    basic_jvm = [{'rules': [{'action': 'allow', 'os': {'name': 'osx'}}], 'value': ['-XstartOnFirstThread']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows'}}], 'value': [
                     '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows', 'version': '^10\\.'}}],
                  'value': ['-Dos.name=Windows 10', '-Dos.version=10.0']},
                 '-Djava.library.path=${natives_directory}', '-Dminecraft.launcher.brand=${launcher_name}',
                 '-Dminecraft.launcher.version=${launcher_version}', '-cp', '${classpath}']

    game_directory = os.path.realpath(game_directory)

    if "MS_refresh_token" in account:
        account = core.auth.oauth.refresh_token(account)

    verpath = os.path.join(game_directory, "versions", version_name)
    libpath = os.path.join(game_directory, "libraries")
    nativepath = os.path.join(verpath, "natives-" + core.system.SystemAndArch.system())
    jsonpath = os.path.join(verpath, version_name + ".json")
    jarpath = os.path.join(verpath, version_name + ".jar")
    assetspath = os.path.join(game_directory, "assets")

    if standalone: game_directory = verpath

    if not (os.path.exists(game_directory) and os.path.exists(jsonpath) and version_name != ""): return False

    ver_json = json.load(open(jsonpath))

    cmdlist.append(java_path)

    cmdlist.append("-Xmx" + str(java_ram) + "m")
    if use_jvm_for_performance:
        cmdlist.append("-XX:+UnlockExperimentalVMOptions")
        cmdlist.append("-XX:+UseParallelGC")
        cmdlist.append("-XX:-OmitStackTraceInFastThrow")
        cmdlist.append("-XX:-DontCompileHugeMethods")
        cmdlist.append("-Dlog4j2.formatMsgNoLookups=true")
        cmdlist.append("-Djava.rmi.server.useCodebaseOnly=true")
        cmdlist.append("-Dcom.sun.jndi.cosnaming.object.trustURLCodebase=false")

    args = []
    if "arguments" in ver_json:
        for i in ver_json["arguments"]["jvm"]:
            if type(i) == str:
                cmdlist.append(i)
            elif _checkRules(i["rules"]):
                if type(i["value"]) == str:
                    cmdlist.append(i["value"])
                else:
                    for j in i["value"]: cmdlist.append(j)
        for i in ver_json["arguments"]["game"]:
            if type(i) == str: args.append(i)
    else:
        args = ver_json["minecraftArguments"].split(" ")
        for i in basic_jvm:
            if type(i) == str:
                cmdlist.append(i)
            elif _checkRules(i["rules"]):
                for j in i["value"]: cmdlist.append(j)

    cmdlist.append("${mainClass}")
    cmdlist += args

    cp = ""

    for i in ver_json['libraries']:  # 遍历libraries数组
        if "name" in i:
            name = i["name"].split(":")  # <package>:<name>:<version>
            name[0] = name[0].replace(".", os.sep)
            p, n, v = name[0], name[1], name[2]  # 分配package, name, version
            rpath = os.path.join(libpath, p, n, v, n + "-" + v + ".jar")  # 获取jar path
            if ("rules" not in i) or _checkRules(i["rules"]):  # 如果未指定规则或者符合规则，就执行操作
                if ("downloads" not in i) or ("classifiers" not in i["downloads"]):
                    cp += os.path.realpath(rpath) + os.pathsep

    cp += jarpath  # 最终将Minecraft核心传入classpath

    arg = {
        "${mainClass}": ver_json["mainClass"],
        "${natives_directory}": nativepath,
        "${launcher_name}": "FMCL",
        "${launcher_version}": "Preview",
        "${classpath}": cp,
        "${assets_root}": assetspath,
        "${assets_index_name}": ver_json["assetIndex"]["id"],
        "${auth_uuid}": account["uuid"],
        "${auth_access_token}": account["access_token"],
        "${user_type}": "Mojang",
        "${version_type}": "FMCL",
        "${user_properties}": "{}",
        "${auth_session}": "{}",
        "${clientid}": "0",
        "${auth_xuid}": "0",
        "${game_assets}": "resources",
        "${auth_player_name}": account["username"],
        "${version_name}": version_name,
        "${game_directory}": game_directory
    }  # 这一串东西是字符串替换模板，用于设置正确的jvm/game参数

    for i in range(len(cmdlist)):  # 循环替换字符串模板
        for j in arg:
            cmdlist[i] = cmdlist[i].replace(j, arg[j])

    return subprocess.list2cmdline(cmdlist), account
