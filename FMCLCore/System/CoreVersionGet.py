import os

import requests


def add(o):
    if " " in o:
        return '"'+o+'"'
    return o


def get_version_list(version_type: list):
    versions = []
    for i in requests.get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json").json()['versions']:
        if i["type"] in version_type:
            versions.append(i["id"])
    return versions


def local_version(mcpath):
    versions = []
    for i in os.listdir(os.path.join(mcpath, "versions")):
        if os.path.exists(os.path.join(mcpath, "versions", i, f"{i}.json")):
            versions.append(i)
    return versions


def java_versions():
    possible = ["Java", "BellSoft", "AdoptOpenJDK", "Zulu", "Microsoft", "Eclipse Foundation", "Semeru"]
    versions = ["java"]
    for i in os.getenv("path").split(";"):
        check = os.path.join(i, "java.exe")
        if os.path.exists(check):
            versions.append(check)
        check = os.path.join(i, "bin", "java.exe")
        if os.path.exists(check):
            versions.append(check)
    for i in possible:
        check1 = os.path.join(os.getenv("ProgramFiles"), i)
        check2 = os.path.join(os.getenv("ProgramFiles(x86)"), i)
        if os.path.exists(check1):
            for j in os.listdir(check1):
                if os.path.exists(os.path.join(check1, j, "bin", "java.exe")):
                    versions.append(os.path.join(os.getenv("ProgramFiles"), i, j, "bin", "java.exe"))
        if os.path.exists(check2):
            for j in os.listdir(check2):
                if os.path.exists(os.path.join(check2, j, "bin", "java.exe")):
                    versions.append(os.path.join(os.getenv("ProgramFiles(x86)"), i, j, "bin", "java.exe"))

    return versions
