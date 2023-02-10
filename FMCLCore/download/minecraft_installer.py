# coding:utf-8
"""
    Minecraft原版的下载
"""
import FMCLCore.system.CoreConfigIO as config
import json
import os
import urllib.request


class MinecraftInstaller(object):
    """
        Minecraft原版下载器
    """

    def __init__(self):
        if os.path.exists(".fmcl_version_meta.json"):
            self.refresh(config.get("source"))
        else:
            self.version_list = json.load(open(".fmcl.version_meta.json", "rb+"))

    def refresh(self, download_source: str = "Default") -> bool:
        """
            刷新版本列表
            :param download_source: 下载源
            :return: 刷新是否成功
        """
        if download_source == "Default":
            manifest = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        elif download_source == "BMCLAPI":
            manifest = "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"
        elif download_source == "MCBBS":
            manifest = "https://download.mcbbs.net/mc/game/version_manifest_v2.json"
        else:
            return False
        information = urllib.request.urlopen(manifest).read()
        with open(".fmcl.version_meta.json", "w") as f:
            f.write(information)
        self.version_list = json.loads(information)

    def get(self, version_types, refresh=False, download_source: str = "Default"):
        """
            获取版本列表
            :param version_types: 需要的版本
            :param download_source: 下载源
            :param refresh: 是否需要刷新
            :return: 最新正式版, 最新快照版, 版本列表
        """
        if refresh:
            self.refresh(download_source)

        version_list = []

        lt_release, lt_snapshot = self.version_list["latest"]["release"], self.version_list["latest"]["snapshot"]

        for i in self.version_list["versions"]:
            if i["id"] == lt_release:
                lt_release = i
            if i["id"] == lt_snapshot:
                lt_snapshot = i
            if i["type"] in version_types:
                version_list.append(i)

        return lt_release, lt_snapshot, version_list


installer = MinecraftInstaller()
