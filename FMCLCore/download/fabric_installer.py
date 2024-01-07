# coding:utf-8
"""
    Fabric的下载与安装
"""
import json
import logging
import os
import subprocess
import urllib.request


class FabricInstaller(object):
    """
        Fabric下载器
    """

    def __init__(self):
        self.game_versions = None
        self.installer_url = None

    def refresh(self) -> None:
        """
            刷新版本列表
            :return: 无
        """
        buf = []
        # 获取支持的游戏版本
        logging.info("Getting game versions from https://meta.fabricmc.net/v2/versions/game")
        for i in json.loads(urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/game").read().decode()):
            buf.append(i["version"])
        self.game_versions = buf
        # 获取安装器
        logging.info("Getting fabric installer from https://meta.fabricmc.net/v2/versions/game")
        self.installer_url = \
            json.loads(urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/installer").read().decode())[0][
                "url"]

    def get_loader_versions(self, mc_version: str) -> list:
        """
            获取游戏版本支持的加载器
            :param mc_version: 游戏版本
            :return: 支持的加载器名称列表
        """
        if mc_version in self.game_versions:
            buf = []
            for i in json.loads(urllib.request.urlopen(
                    "https://meta.fabricmc.net/v2/versions/loader/" + mc_version).read().decode()):
                print(i)
                buf.append(i["loader"]["version"])
            return buf
        else:
            return []

    def install(self, java: str, mc_path: str, mc_version: str, fabric_version: str) -> None:
        """
            安装Fabric
            :param java: java路径
            :param mc_path: .minecraft路径
            :param mc_version: Minecraft版本
            :param fabric_version: Fabric版本
            :return: 无
        """
        with open(os.path.join(mc_path, "fabricinstaller.jar"), "wb") as f:
            response = urllib.request.urlopen(self.installer_url, timeout=5)
            data = response.read(128)
            while data:
                f.write(data)
                data = response.read(128)
        subprocess.run([java,
                        "-jar", os.path.join(mc_path, "fabricinstaller.jar"),
                        "client",
                        "-dir", mc_path,
                        "-mcversion", mc_version,
                        "-loader", fabric_version])


installer = FabricInstaller()
