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
import core.local.system_scanner
from core.local.system_scanner import get_system


def _checkRules(rules: dict):
    for i in rules:
        if i["action"] == "allow":
            if "os" in i:
                if "name" in i["os"] and get_system() != i["os"]["name"]:
                    return False
                elif "version" in i["os"] and not re.match(i["os"]["version"], platform.version()):
                    return False
        elif i["action"] == "disallow":
            if "os" in i:
                if "name" in i["os"] and get_system() == i["os"]["name"]:
                    return False
                elif "version" in i["os"] and re.match(i["os"]["version"], platform.version()):
                    return False
    return True


class NoSuchVersionException(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return "Could not find version: {}. Please check if it really exists."


def launch(game_directory: str, version_name: str, account: dict,
           java_path: str = "java", java_ram: int = 1024, use_better_jvm: bool = False,
           standalone: bool = False) -> list[list[str], dict]:
    """
    :param game_directory: .minecraft文件夹路径
    :param version_name: 启动的版本名
    :param account: 启动的账号
    :param java_path: java运行时路径
    :param java_ram: java虚拟机内存（即分配给游戏的内存）
    :param use_better_jvm: 使用优化jvm参数
    :param standalone: 启用版本隔离
    :return: 启动的命令行，更新后的账号
    """

    # 初始化空的命令行
    cmdlist = []

    # 若目标版本没有jvm，则使用默认值
    basic_jvm = [{'rules': [{'action': 'allow', 'os': {'name': 'osx'}}], 'value': ['-XstartOnFirstThread']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows'}}], 'value': [
                     '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump']},
                 {'rules': [{'action': 'allow', 'os': {'name': 'windows', 'version': '^10\\.'}}],
                  'value': ['-Dos.name=Windows 10', '-Dos.version=10.0']},
                 '-Djava.library.path=${natives_directory}', '-Dminecraft.launcher.brand=${launcher_name}',
                 '-Dminecraft.launcher.version=${launcher_version}', '-cp', '${classpath}']

    game_directory = os.path.realpath(game_directory)

    # 如果是微软账户，就刷新账户
    if "MS_refresh_token" in account:
        account = core.auth.oauth.refresh_token(account)

    verpath = os.path.join(game_directory, "versions", version_name)  # 版本路径
    libpath = os.path.join(game_directory, "libraries")  # 依赖库路径
    nativepath = os.path.join(verpath, "natives-" + get_system())  # 动态链接库路径
    jsonpath = os.path.join(verpath, version_name + ".json")  # version.json路径
    jarpath = os.path.join(verpath, version_name + ".jar")  # version.jar路径
    assetspath = os.path.join(game_directory, "assets")  # 资源索引路径

    if standalone: game_directory = verpath

    # 如果版本或者版本json不存在，抛出异常
    if not (os.path.isdir(game_directory) and os.path.isfile(jsonpath) and version_name):
        raise NoSuchVersionException(version_name)

    ver_json = json.load(open(jsonpath))

    cmdlist.append(java_path)

    cmdlist.append("-Xmx" + str(java_ram) + "m")
    if use_better_jvm:
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
