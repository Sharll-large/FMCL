# coding:utf-8
# TODO: 重构为单例
import json
import os
import urllib.request


def add(o):
    if " " in o:
        return '"' + o + '"'
    return o


def get_version_list(version_type: list):
    versions = []
    for i in json.loads(
            urllib.request.urlopen("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json").read()
    )["versions"]:
        if i["type"] in version_type:
            versions.append(i["id"])
    return versions


def local_version(mcpath):
    versions = []
    for i in os.listdir(os.path.join(mcpath, "versions")):
        if os.path.exists(os.path.join(mcpath, "versions", i, f"{i}.json")):
            versions.append(i)
    return versions
