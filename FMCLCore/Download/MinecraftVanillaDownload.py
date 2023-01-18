import json
import urllib.request


class Downloader:
    def __init__(self, download_source: str = "Default"):
        self.version_list = None
        if download_source == "Default": self.manifest = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        elif download_source == "BMCLAPI": self.manifest = "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"
        elif download_source == "MCBBS": self.manifest = "https://download.mcbbs.net/mc/game/version_manifest_v2.json"
        self.refresh()

    def refresh(self):
        self.version_list = json.loads(urllib.request.urlopen(self.manifest).read())

    def get(self, version_types: list[str]):
        temp = {}
        for i in self.version_list["versions"]:
            if i["type"] in version_types:
                temp[i["id"]] = {
                    "type": i["type"],
                    "url": i["url"],
                    "time": i["time"],
                    "releaseTime": i["releaseTime"],
                    "sha1": i["sha1"]
                }
        return temp

    def get_latest(self):
        return {
            "snapshot": self.get(["release", "snapshot"])[self.version_list["latest"]["release"]],
            "release": self.get(["release"])[self.version_list["latest"]["release"]]
        }


downloader = Downloader("Default")
refresh = downloader.refresh
get = downloader.get
get_latest = downloader.get_latest


