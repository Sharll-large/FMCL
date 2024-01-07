# coding:utf-8
import requests


def _get_forge_versions(mcversion: str):
    a = requests.get(f"https://files.minecraftforge.net/net/minecraftforge/forge/maven-metadata.json").json()
    if mcversion in a:
        return a[mcversion]
    else:
        return []


def _get_forge_url(version: str):
    return "https://maven.minecraftforge.net/net/minecraftforge/forge/" + version + \
        "/forge-" + version + \
        "-installer.jar"
