import json
import os
import os.path
import threading
import zipfile
import tkinter.messagebox
import Core.System.CoreSystemInformation

import requests

import Core.System.CoreMakeFolderTask

paths = []
urls = []
nativesjar = []


def _get_ver_jar_url(version: str):
    for i in requests.get("https://piston-meta.mojang.com/mc/game/version_manifest.json").json()['versions']:
        if i["id"] == version:
            return i["url"]


def get_task(version_name: str, version: str, mcpath: str):
    assets = "https://resources.download.minecraft.net"

    global paths, urls, nativesjar
    paths = []
    urls = []
    nativesjar = []

    if os.path.exists(os.path.join(mcpath, "versions", version_name)):
        tkinter.messagebox.showinfo("Info", "The folder is exist. Launch fixing mode.")

    # create game folder
    Core.System.CoreMakeFolderTask.make_long_dir(os.path.join(mcpath, "versions", version_name))

    # download version json

    open(os.path.join(mcpath, "versions", version_name, version_name + ".json"), "wb").write(requests.get(_get_ver_jar_url(version)).content)
    ver_json = json.load(open(os.path.join(mcpath, "versions", version_name, version_name + ".json")))

    # add version.jar to task
    urls.append(f"{ver_json['downloads']['client']['url']}")
    paths.append(os.path.join(mcpath, "versions", version_name, version_name + ".jar"))

    # natives
    for i in ver_json["libraries"]:
        if "downloads" in i:
            print("basic download")
            if "artifact" in i["downloads"]:
                urls.append(i["downloads"]["artifact"]["url"])
                paths.append(os.path.join(mcpath, "libraries", i["downloads"]["artifact"]["path"]))

            elif ("classifiers" in i["downloads"]) and "natives-" + Core.System.CoreSystemInformation.system() in \
                    i["downloads"]["classifiers"]:
                print(i)

                urls.append(i["downloads"]["classifiers"]["natives-windows"]["url"])
                paths.append(os.path.join(mcpath, "libraries", i["downloads"]["classifiers"]["natives-windows"]["path"]))
                nativesjar.append(os.path.join(mcpath, "libraries", i["downloads"]["classifiers"]["natives-windows"]["path"]))
        elif "url" in i:
            print("Find url in this object.")
            name = i["name"].split(":")  # <package>:<name>:<version>
            name[0] = name[0].replace(".", "/")
            package = name[0]
            name = name[1]
            version = name[2]
            urls.append(os.path.join(i["url"], package, name, version, name + "-" + version + ".jar").replace("\\", "/"))
            paths.append(os.path.join(mcpath, package, name, version, name + "-" + version + ".jar"))
        else:
            print()
        # if "extract" in i:
        #     print(i)

    # assets
    Core.System.CoreMakeFolderTask.make_dir(os.path.join(mcpath, "assets", "indexes"))
    Core.System.CoreMakeFolderTask.make_dir(os.path.join(mcpath, "assets", "objects"))
    open(f"{mcpath}/assets/indexes/{ver_json['assetIndex']['id']}.json", "wb").write(requests.get(ver_json['assetIndex']['url']).content)

    index_json = json.load(open(f"{mcpath}/assets/indexes/{ver_json['assetIndex']['id']}.json"))
    for i in index_json["objects"]:
        now_hash = index_json["objects"][i]["hash"]
        urls.append(f"{assets}/{now_hash[0:2]}/{now_hash}")
        os.path.join(mcpath, "assets", "objects", now_hash[0:2], now_hash)
        paths.append(f"{mcpath}/assets/objects/{now_hash[0:2]}/{now_hash}")

    # log4j config
    Core.System.CoreMakeFolderTask.make_long_dir(f"{mcpath}\\versions\\{version_name}")
    urls.append(ver_json["logging"]["client"]["file"]["url"])
    paths.append(f"{mcpath}\\versions\\{version_name}\\log4j2.xml")


def multprocessing_task(tasks: list, function, cores: int, join: bool = True):
    threads = []

    def _run():
        while threads:
            try:
                task = tasks.pop(0)
                function(task)
            except Exception:
                break

    for i in range(cores + 1):
        thread = threading.Thread(target=_run)
        thread.start()
        threads.append(thread)

    if join:
        for thread in threads:
            thread.join()


def download_one(i):
    url = i[0]
    path = i[1]
    if not os.path.exists(os.path.realpath(path)):
        Core.System.CoreMakeFolderTask.make_long_dir(os.path.dirname(path))
        open(os.path.realpath(path), "wb").write(requests.get(url).content)


def download(ver_name: str, version: str, mcpath: str, threads: int):
    get_task(ver_name, version, mcpath)
    tasks = []
    for i in range(len(urls)):
        tasks.append((urls[i], paths[i]))
    multprocessing_task(tasks, download_one, threads, True)

    for i in nativesjar:
        print(i)
        jar = os.path.realpath(i)
        Core.System.CoreMakeFolderTask.make_long_dir(os.path.realpath(
            f'{os.path.realpath(mcpath)}/versions/{ver_name}/natives-windows-x86_64'))
        zip_file = zipfile.ZipFile(jar)
        for names in zip_file.namelist():
            zip_file.extract(names, os.path.realpath(
                f'{os.path.realpath(mcpath)}/versions/{ver_name}/natives-windows-x86_64'))
