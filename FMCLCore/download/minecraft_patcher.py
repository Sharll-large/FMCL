# coding: utf-8
"""
    补全minecraft依赖和资源文件
"""

import hashlib
import json
import os
import platform
import re
import threading
import urllib.parse
import urllib.request

import FMCLCore.system.SystemAndArch
import FMCLCore.system.UnzipTask
import FMCLCore.system.thread_pool


def download_native(arg: dict) -> None:
    """
        下载动态链接库
        :param arg: 下载设置
        :return: 无
    """
    back_msg = threading.current_thread().name + " done with message: "
    e = 0
    emsg = ""
    for i in range(5):
        if os.path.exists(arg["path"]) and \
                (("size" not in arg) or (os.path.getsize(arg["path"]) == arg["size"])) and \
                (("sha1" not in arg) or (hashlib.sha1(open(arg["path"], "rb").read()).hexdigest() == arg["sha1"])):
            if "unzip" in arg:
                FMCLCore.system.UnzipTask.unzip(arg["path"], arg["unzip"])
            back_msg += f"Download successfully in {i} try(s) and {e} exception(s): {emsg}"
            break
        else:
            try:
                open(arg["path"], "wb+").write(urllib.request.urlopen(arg["url"], timeout=5).read())
            except Exception as exc:
                e += 1
                emsg += repr(exc)
    print(back_msg)


def _checkRules(rules: dict):
    for i in rules:
        if i["action"] == "allow":
            if "os" in i:
                if "name" in i["os"] and FMCLCore.system.SystemAndArch.system() != i["os"]["name"]:
                    return False
                elif "version" in i["os"] and not re.match(i["os"]["version"], platform.version()):
                    return False
        elif i["action"] == "disallow":
            if "os" in i:
                if "name" in i["os"] and FMCLCore.system.SystemAndArch.system() == i["os"]["name"]:
                    return False
                elif "version" in i["os"] and re.match(i["os"]["version"], platform.version()):
                    return False
    return True


def patch(game_directory: str, version_name: str, threads: int = 64, download_source: str = "Default") -> None:
    """
        补全版本
        :param game_directory: 游戏目录
        :param version_name: 版本名称
        :param threads: 核数
        :param download_source: 下载源
        :return: 无
    """

    def convert_url(url: str):  # 若切换了下载源调用此方法转换链接
        for link in down:
            url = url.replace(link, down[link])
        return url

    game_directory = os.path.realpath(game_directory)

    if download_source == "Default":
        down = {}
    elif download_source == "MCBBS":
        down = {
            "https://resources.download.minecraft.net/": "https://download.mcbbs.net/assets/",
            "https://libraries.minecraft.net/": "https://download.mcbbs.net/maven/",
            "https://files.minecraftforge.net/maven/": "https://download.mcbbs.net/maven/",
            "https://maven.fabricmc.net/": "https://download.mcbbs.net/maven/"
        }
    elif download_source == "BMCLAPI":
        down = {
            "https://resources.download.minecraft.net/": "https://bmclapi2.bangbang93.com/assets/",
            "https://libraries.minecraft.net/": "https://bmclapi2.bangbang93.com/maven/",
            "https://files.minecraftforge.net/maven/": "https://bmclapi2.bangbang93.com/maven/",
            "https://maven.fabricmc.net/": "https://bmclapi2.bangbang93.com/maven/"
        }

    version_path = os.path.join(game_directory, "versions", version_name)
    libpath = os.path.join(game_directory, "libraries")
    native_path = os.path.join(version_path, "natives-" + FMCLCore.system.SystemAndArch.system())
    jsonpath = os.path.join(version_path, version_name + ".json")
    jar_path = os.path.join(version_path, version_name + ".jar")
    assets_path = os.path.join(game_directory, "assets")
    ver_json = json.load(open(jsonpath))
    assets_index_path = os.path.join(assets_path, "indexes", ver_json["assetIndex"]["id"] + ".json")
    assets_object_path = os.path.join(assets_path, "objects")

    need_to_be_fixed = []

    if not os.path.exists(jar_path):
        need_to_be_fixed.append({
            "path": jar_path,
            "url": convert_url(ver_json["downloads"]["client"]["url"]),
            "size": ver_json["downloads"]["client"]["size"],
            "sha1": ver_json["downloads"]["client"]["sha1"]})

    if not os.path.exists(assets_index_path):
        FMCLCore.system.CoreMakeFolderTask.make_long_dir(os.path.dirname(assets_index_path))
        download_native({
            "path": assets_index_path,
            "url": convert_url(ver_json["assetIndex"]["url"]),
            "size": ver_json["assetIndex"]["size"],
            "sha1": ver_json["assetIndex"]["sha1"]
        })

    for i in ver_json['libraries']:  # 遍历libraries数组
        if "name" in i:
            name = i["name"].split(":")  # <package>:<name>:<version>
            name[0] = name[0].replace(".", os.sep)
            p, n, v = name[0], name[1], name[2]  # 分配package, name, version
            rpath = os.path.join(libpath, p, n, v, n + "-" + v + ".jar")  # 获取jar path
            if ("rules" not in i) or _checkRules(i["rules"]):  # 如果未指定规则或者符合规则，就执行操作
                if ("downloads" not in i) or ("classifiers" not in i["downloads"]):
                    if "downloads" in i and "artifact" in i["downloads"]:
                        if "path" in i["downloads"]["artifact"]:
                            path = os.path.join(libpath, i["downloads"]["artifact"]["path"])
                        else:
                            path = rpath
                        package = {
                            "path": path,
                            "url": convert_url(i["downloads"]["artifact"]["url"]),
                            "size": i["downloads"]["artifact"]["size"],
                            "sha1": i["downloads"]["artifact"]["sha1"]
                        }
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        need_to_be_fixed.append(package)
                    elif "url" in i:
                        os.makedirs(os.path.dirname(rpath), exist_ok=True)
                        need_to_be_fixed.append({
                            "path": rpath,
                            "url": i["url"] + p.replace("\\", "/") + "/" + n + "/" + v + "/" + n + "-" + v + ".jar"})
                    else:
                        pass

                else:  # 若不是只有artifact键，则认为这是natives，下载并解压
                    rname = i["natives"][FMCLCore.system.SystemAndArch.system()].replace("${arch}",
                                                                                         platform.architecture()[
                                                                                             0].replace("bit", ""))
                    if "path" in i["downloads"]["classifiers"][rname]:
                        path = os.path.join(libpath, i["downloads"]["classifiers"][rname]["path"])
                    else:
                        path = rpath
                    package = {
                        "path": path,
                        "url": convert_url(i["downloads"]["classifiers"][rname]["url"]),
                        "unzip": native_path,
                        "size": i["downloads"]["classifiers"][rname]["size"],
                        "sha1": i["downloads"]["classifiers"][rname]["sha1"]
                    }
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    need_to_be_fixed.append(package)

    assets_json = json.load(open(assets_index_path))["objects"]
    for i in assets_json:
        path = os.path.join(assets_object_path, assets_json[i]["hash"][0:2], assets_json[i]["hash"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        need_to_be_fixed.append({
            "path": path,
            "url": convert_url(
                "https://resources.download.minecraft.net/" + assets_json[i]["hash"][0:2] + "/" + assets_json[i][
                    "hash"]),
            "sha1": assets_json[i]["hash"],
            "size": assets_json[i]["size"]
        })

    processes = []
    for i in need_to_be_fixed:
        print(i)
        processes.append(FMCLCore.system.thread_pool.pool.submit(download_native, i))

    # 堵塞主线程，直到所有下载完成
    flg = True
    while flg:
        flg = False
        for i in processes:
            if not i.done():
                flg = True
